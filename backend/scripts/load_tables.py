"""
This script uses playwright to scrape over all tables present on the "Base dos Dados" page,
after downloading the files and loading into a dataframe, inserts all records on the database
"""

import asyncio

import errno
import logging.config
import os
from pathlib import Path
import shutil

from dotenv import load_dotenv
from sqlalchemy import MetaData, Table
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine
from sqlalchemy.sql.expression import insert
from playwright.async_api import Locator, async_playwright, Page, Browser
import polars as pl

LOGGING_CONFIG = {
    "version": 1,
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stderr",
        },
    },
    "formatters": {
        "default": {
            "format": "%(levelname)s [%(asctime)s] %(filename)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["default"],
    },
}
logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger(__name__)

load_dotenv()

BASE_TABLES_URL = (
    "https://basedosdados.org/dataset/51ee8a6c-e410-4fc2-b2a4-e778c5b1ef3d"
)
RAW_DATA_URL = "https://dados.ons.org.br/dataset/balanco-energia-subsistema"


# maps each csv file name to
schemas_for_csv = {
    "BALANCO_ENERGIA_SUBSISTEMA": (
        "balanco_subsistema_horario",
        pl.Schema(
            {
                "id_subsistema": pl.String(),
                "nom_subsistema": pl.String(),
                "din_instante": pl.Datetime(),
                "val_gerhidraulica": pl.Float64(),
                "val_gertermica": pl.Float64(),
                "val_gereolica": pl.Float64(),
                "val_gersolar": pl.Float64(),
                "val_carga": pl.Float64(),
                "val_intercambio": pl.Float64(),
            }
        ),
    ),
    "br_ons_estimativa_custos_balanco_energia_subsistemas_dessem": (
        "balanco_subsistema_semihorario",
        pl.Schema(
            {
                "data": pl.Date(),
                "hora": pl.Time(),
                "id_subsistema": pl.String(),
                "subsistema": pl.String(),
                "usina_hidraulica_verificada": pl.Float64(),
                "geracao_eolica_verificada": pl.Float64(),
                "geracao_fotovoltaica_verificada": pl.Float64(),
                "geracao_usina_termica_verificada": pl.Float64(),
                "geracao_pequena_usina_hidraulica_verificada": pl.Float64(),
                "geracao_pequena_usina_termica_verificada": pl.Float64(),
            }
        ),
    ),
    "br_ons_estimativa_custos_custo_marginal_operacao_semanal": (
        "custo_marginal_operacao_semanal",
        pl.Schema(
            {
                "data": pl.Date(),
                "id_subsistema": pl.String(),
                "subsistema": pl.String(),
                "custo_marginal_operacao_semanal": pl.Float64(),
                "custo_marginal_operacao_semanal_carga_leve": pl.Float64(),
                "custo_marginal_operacao_semanal_carga_media": pl.Float64(),
                "custo_marginal_operacao_semanal_carga_pesada": pl.Float64(),
            }
        ),
    ),
    "br_ons_estimativa_custos_custo_marginal_operacao_semi_horario": (
        "custo_marginal_operacao_semihorario",
        pl.Schema(
            {
                "data": pl.Date(),
                "hora": pl.Time(),
                "id_subsistema": pl.String(),
                "subsistema": pl.String(),
                "custo_marginal_operacao": pl.Float64(),
            }
        ),
    ),
    "br_ons_estimativa_custos_custo_variavel_unitario_usinas_termicas": (
        "custo_variavel_unitario_usinas_termicas",
        pl.Schema(
            {
                "data_inicio": pl.Date(),
                "data_fim": pl.Date(),
                "semana_operativa": pl.String(),
                "id_modelo_usina": pl.String(),
                "id_subsistema": pl.String(),
                "subsistema": pl.String(),
                "usina": pl.String(),
                "custo_variavel_unitario": pl.Float64(),
            }
        ),
    ),
}

# maps the column names on the csv files to the column names to be used on the database
table_mapping_for_csv = {
    # commom columns
    "din_instante": "instante",
    "nom_subsistema": "nome_subsistema",
    "subsistema": "nome_subsistema",
    # raw data columns
    "val_gerhidraulica": "geracao_hidraulica",
    "val_gertermica": "geracao_termica",
    "val_gereolica": "geracao_eolica",
    "val_gersolar": "geracao_solar",
    "val_carga": "valor_carga",
    "val_intercambio": "valor_intercambio",
    # verified columns (DESSEM)
    "usina_hidraulica_verificada": "geracao_hidraulica",
    "geracao_pequena_usina_hidraulica_verificada": "geracao_hidraulica_pequena_usina",
    "geracao_usina_termica_verificada": "geracao_termica",
    "geracao_pequena_usina_termica_verificada": "geracao_termica_pequena_usina",
    "geracao_eolica_verificada": "geracao_eolica",
    "geracao_fotovoltaica_verificada": "geracao_solar",
}


async def main():
    DATABASE_URL = os.getenv("DATABASE_URL")

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL not set")

    try:
        raw_data_paths, treated_data_paths = await scrape_tables()

        # for every table stores a tuple with the table name and the corresponding dataframe
        data_for_table_name: list[tuple[str, pl.DataFrame]] = []

        data_for_table_name.append(get_raw_data(raw_data_paths))

        for treated in treated_data_paths:
            data_for_table_name.append(_read_csv(treated))

        engine = create_async_engine(DATABASE_URL)
        async with engine.begin() as conn:
            metadata = MetaData()
            await conn.run_sync(metadata.reflect)
            tables_dict = metadata.tables

            try:
                # all tables have information about subsystems, choosing the first one
                # by convention
                await _insert_on_table(
                    "subsistema",
                    tables_dict,
                    data_for_table_name[0][1],
                    conn,
                    unique=True,
                )
                for table_name, data in data_for_table_name:
                    await _insert_on_table(table_name, tables_dict, data, conn)
                await conn.commit()
                logger.info("Successfully pulled table info from csv files")
            except Exception:
                logger.exception("Error saving data on tables")
                await conn.rollback()

    finally:
        try:
            shutil.rmtree(os.path.join(os.path.dirname(__file__), "csv"))
        except OSError as e:
            if e.errno != errno.ENOENT:
                logger.error(f"Unexpected error removing csv files: code {e.errno}")


async def _insert_on_table(
    table_name: str,
    tables_dict: dict[str, Table],
    dataframe: pl.DataFrame,
    connection: AsyncConnection,
    unique: bool = False,
):
    if table_name not in tables_dict:
        logger.error(f"Table {table_name} do not exists in the database")
        raise ValueError(f"Missing table {table_name}")

    logger.info(f"Starting conversion of dataframe to table {table_name}")
    table = tables_dict[table_name]
    insertion_columns = table.columns.keys()

    # ignoring auto-generated id on tables
    try:
        insertion_columns.remove("id")
    except ValueError:
        pass

    df = dataframe.rename(table_mapping_for_csv, strict=False).select(insertion_columns)
    if unique:
        df = df.unique()

    records = df.to_dicts()

    statement = insert(table)

    logger.info(f"Inserting {len(records)} rows on table {table_name}")
    _ = await connection.execute(statement, records)


def get_raw_data(raw_files: list[str]) -> tuple[str, pl.DataFrame]:
    dataframe_for_table = [_read_csv(file, separator=";") for file in raw_files]

    result_df = pl.concat([pair[1] for pair in dataframe_for_table])
    return dataframe_for_table[0][0], result_df


async def scrape_tables() -> tuple[list[str], list[str]]:
    logger.info(f"Starting scraping of csv files in path {BASE_TABLES_URL}")
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        response = await page.goto(BASE_TABLES_URL)

        helper_text_identifier = "Tabelas tratadas"

        if not response or response.status == 404:
            raise ValueError(f"Couldn't access page {BASE_TABLES_URL}")

        table_links_helper_text = await page.locator(
            "p", has_text=helper_text_identifier
        ).all()

        if len(table_links_helper_text) > 1:
            raise ValueError(
                f"More than one occurrence of text '{helper_text_identifier}' identified, can't proceed"
            )

        clickable_links = await (
            table_links_helper_text[0]
            .locator("xpath=following-sibling::div")
            .locator("p")
        ).all()

        # download the first table on the original font
        raw_data_paths = await _download_original_tables(browser, RAW_DATA_URL)

        treated_data_paths: list[str] = []
        # navigating to next table before download csv because first table is not available on the website
        for link in clickable_links[1:]:
            await link.click()
            treated_data_paths.append(await _download_csv(page))

    logger.info("Finished scraping for csv files")
    return (raw_data_paths, treated_data_paths)


async def _download_original_tables(browser: Browser, url: str) -> list[str]:
    logger.info(
        "Opening new page to get raw files for table 'Balanço de Energia por Subsistema'"
    )
    page = await browser.new_page()
    response = await page.goto(url)
    if not response or response.status == 404:
        raise ValueError(f"Couldn't access page {url}")

    resources = await page.locator("li.resource-item").all()

    paths: list[str] = []
    for resource in resources:
        download = await _download_raw_csv_resource(page, resource)
        if download:
            paths.append(download)

    return paths


async def _download_raw_csv_resource(page: Page, resource: Locator) -> str | None:
    if await resource.locator('span[data-format="csv"]').count() > 0:
        async with page.expect_download() as download_info:
            resource_download_url = resource.locator("a.resource-url-analytics")
            await resource_download_url.dispatch_event("click")
        download = await download_info.value
        path = os.path.join(
            os.path.dirname(__file__),
            "csv/balanco-energia",
            download.suggested_filename,
        )
        logger.info(f"saving csv file on path {path}")
        await download.save_as(path)
        return path


async def _download_csv(page: Page) -> str:
    download_tab_text_identifier = "download"
    download_tab_buttons = await page.get_by_role(role="tab", name="download").all()
    if len(download_tab_buttons) > 1:
        raise ValueError(
            f"More than one occurrence of text '{download_tab_text_identifier}' identified, can't proceed"
        )

    button = download_tab_buttons[0]
    await button.click()

    download_table_button_text = "Download da tabela"
    download_button_elements = await page.locator(
        "button", has_text=download_table_button_text
    ).all()

    if len(download_button_elements) > 1:
        raise ValueError(
            f"More than one occurrence of text '{download_table_button_text}' identified, can't proceed"
        )
    download_button = download_button_elements[0]

    async with page.expect_download() as download_info:
        await download_button.click()
    download = await download_info.value
    path = os.path.join(os.path.dirname(__file__), "csv", download.suggested_filename)

    logger.info(f"saving csv file on path {path}")
    await download.save_as(path)
    return path


def _read_csv(path_str: str, separator: str = ",") -> tuple[str, pl.DataFrame]:
    path = Path(path_str)
    full_filename = path.parts[-1]
    filename_no_suffixes = full_filename.split(".")[0]

    if filename_no_suffixes.startswith("BALANCO_ENERGIA_SUBSISTEMA"):
        used_schema = schemas_for_csv["BALANCO_ENERGIA_SUBSISTEMA"]
    else:
        used_schema = schemas_for_csv[filename_no_suffixes]

    df = pl.read_csv(
        source=path_str,
        columns=used_schema[1].names(),
        schema_overrides=used_schema[1],
        separator=separator,
    )

    # needed only raw data that doesn't include date and time columns
    if "din_instante" in df.columns and (
        "data" not in df.columns or "hora" not in df.columns
    ):
        df = df.with_columns(
            [
                pl.col("din_instante").dt.date().alias("data"),
                pl.col("din_instante").dt.time().alias("hora"),
            ]
        )

    return used_schema[0], df


if __name__ == "__main__":
    asyncio.run(main())
