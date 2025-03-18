from datetime import date
from fastapi import APIRouter, Security
from sqlalchemy import select

from ..core.security import validate_token
from ..crud.energy_statement_crud import EnergyStatementCrud

from ..exceptions.query import InvalidArgumentException


from ..deps import AsyncSessionMakerDep

from ..schemas import EnergyStatementResponse, HalfHourlyEnergyStatementResponse

router = APIRouter(dependencies=[Security(validate_token)])


@router.get("/horario")
async def get_hourly_energy_statements(
    data_inicial: date,
    data_final: date,
    session_maker: AsyncSessionMakerDep,
    limite: int = 500,
    deslocamento: int = 0,
) -> EnergyStatementResponse:
    """
    Retorna o balanço de energia geral com os dados de todos os subsistemas agrupados
    por data e hora de medição. Utiliza as medições no padrão antigo, medidas de hora em
    hora
    """
    if data_inicial > data_final:
        raise InvalidArgumentException(
            "Data inicial não pode ser posterior à data final"
        )
    crud = EnergyStatementCrud(session_maker)
    return await crud.get_hourly_energy_statements(
        data_inicial=data_inicial,
        data_final=data_final,
        limit=limite,
        offset=deslocamento,
    )


@router.get("/semihorario")
async def get_half_hourly_energy_statements(
    data_inicial: date,
    data_final: date,
    session_maker: AsyncSessionMakerDep,
    limite: int = 500,
    deslocamento: int = 0,
) -> HalfHourlyEnergyStatementResponse:
    """
    Retorna o balanço de energia geral com os dados de todos os subsistemas agrupados
    por data e hora de medição. Utiliza as medições no padrão DESSEM, medidas a cada
    meia hora. Os dados estão disponíveis de 2023-08-15 até 2024-03-03
    """
    if data_inicial > data_final:
        raise InvalidArgumentException(
            "Data inicial não pode ser posterior à data final"
        )

    crud = EnergyStatementCrud(session_maker)
    return await crud.get_half_hourly_energy_statements(
        data_inicial=data_inicial,
        data_final=data_final,
        limit=limite,
        offset=deslocamento,
    )
