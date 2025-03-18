from datetime import date
from fastapi import APIRouter, Security

from ..core.security import validate_token

from ..exceptions.query import InvalidArgumentException

from ..crud.marginal_costs_crud import CostCrud
from ..deps import AsyncSessionMakerDep
from ..schemas import (
    HalfHourlySubSystemMarginalCostSchema,
    WeeklySubSystemMarginalCostSchema,
)

router = APIRouter(dependencies=[Security(validate_token)])


@router.get("/semanal")
async def get_weekly_costs(
    data_inicial: date,
    data_final: date,
    session_maker: AsyncSessionMakerDep,
    limite: int = 500,
    deslocamento: int = 0,
) -> list[WeeklySubSystemMarginalCostSchema]:
    """
    Retorna informações do Custo Marginal de Operação de todos os subsistemas agrupadas
    pela semana de medição. Os dados estão disponíveis da primeira semana de 2005
    (07/01/2005) até a primeira semana de março em 2024 (08/03/2025).
    """

    if data_inicial > data_final:
        raise InvalidArgumentException(
            "Data inicial não pode ser posterior à data final"
        )

    crud = CostCrud(session_maker)
    return await crud.get_all_weekly(
        start_date=data_inicial, end_date=data_final, limit=limite, offset=deslocamento
    )


@router.get("/semihorario")
async def get_half_hourly_costs(
    data_inicial: date,
    data_final: date,
    session_maker: AsyncSessionMakerDep,
    limite: int = 500,
    deslocamento: int = 0,
) -> list[HalfHourlySubSystemMarginalCostSchema]:
    """
    Retorna o valor do Custo Marginal de Operação de todos os subsistemas agrupados
    pela data e hora da medição, os intervalos de medição são de 30 minutos
    """
    if data_inicial > data_final:
        raise InvalidArgumentException(
            "Data inicial não pode ser posterior à data final"
        )

    crud = CostCrud(session_maker)
    return await crud.get_all_half_hourly(
        start_date=data_inicial, end_date=data_final, limit=limite, offset=deslocamento
    )
