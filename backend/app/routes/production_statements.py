from datetime import date
from fastapi import APIRouter

router = APIRouter()


@router.get("/horario")
async def get_hourly_energy_statements(
    data_inicial: date,
    data_final: date,
):
    """
    Retorna o balanço de energia geral com os dados de todos os subsistemas agrupados
    por data e hora de medição. Utiliza as medições no padrão antigo, medidas de hora em
    hora
    """


@router.get("/semihorario")
async def get_half_hourly_energy_statements(
    data_inicial: date,
    data_final: date,
):
    """
    Retorna o balanço de energia geral com os dados de todos os subsistemas agrupados
    por data e hora de medição. Utiliza as medições no padrão DESSEM, medidas a cada
    meia hora
    """
