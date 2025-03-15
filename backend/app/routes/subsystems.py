from datetime import date
from typing import Literal
from fastapi import APIRouter, Security
from ..core.security import validate_token


router = APIRouter(dependencies=[Security(validate_token)])


@router.get("/balanco-energia")
def get_energy_statements(
    data_inicial: date, data_final: date, fonte: Literal["Padrao", "Dessem"] = "Padrao"
): ...


@router.get("/custo-semanal")
def get_weekly_costs(data_inicial: date, data_final: date): ...


@router.get("/custo-semihorario")
def get_hourly_costs(data_inicial: date, data_final: date): ...
