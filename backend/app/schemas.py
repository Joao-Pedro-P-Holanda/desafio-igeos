from datetime import date, time
from pydantic import BaseModel, Field


class SubSystem(BaseModel):
    id_subsistema: str
    nome_subsistema: str


class HourlyEnergyStatement(BaseModel):
    id_subsistema: str
    subsistema_nome: str | None = None
    data: date
    hora: time
    geracao_eolica: float | None = None
    geracao_termica: float | None = None
    geracao_solar: float | None = None
    geracao_hidraulica: float | None = None
    valor_carga: float
    valor_intercambio: float


class HalfHourlyEnergyStatement(BaseModel):
    id_subsistema: str
    subsistema_nome: str | None = None
    data: date
    hora: time
    geracao_eolica: float | None = None
    geracao_termica: float | None = None
    geracao_solar: float | None = None
    geracao_hidraulica: float | None = None
    geracao_hidraulica_pequena_usina: float
    geracao_termica_pequena_usina: float


class EnergyStatementResponse(BaseModel):
    total_registros: int
    data_inicial: date
    data_final: date
    dados: list[HourlyEnergyStatement]


class HalfHourlyEnergyStatementResponse(BaseModel):
    total_registros: int
    data_inicial: date
    data_final: date
    dados: list[HalfHourlyEnergyStatement]


