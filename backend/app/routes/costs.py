from datetime import date
from fastapi import APIRouter

router = APIRouter()


@router.get("/semanal")
async def get_weekly_costs(data_inicial: date, data_final: date):
    """
    Retorna informações do Custo Marginal de Operação de todos os subsistemas agrupadas
    pela semana de medição
    """


@router.get("/semihorario")
async def get_hourly_costs(data_inicial: date, data_final: date):
    """
    Retorna o valor do Custo Marginal de Operação de todos os subsistemas agrupados
    pela data e hora da medição, os intervalos de medição são de 30 minutos
    """
