from datetime import date
import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.exceptions.database import NotFoundException

from ..schemas import (
    EnergyStatementResponse,
    HalfHourlyEnergyStatementResponse,
    HalfHourlyEnergyStatement,
    HourlyEnergyStatement,
)

from ..models import (
    HourlySubSystemProductionStatement,
    HalfHourlySubSystemProductionStatement,
)
from ..deps import AsyncSessionMakerDep


class EnergyStatementCrud:
    def __init__(self, session_maker: AsyncSessionMakerDep):
        self._session_maker: async_sessionmaker[AsyncSession] = session_maker

    async def get_hourly_energy_statements(
        self,
        data_inicial: date,
        data_final: date,
        limit: int,
        offset: int,
    ) -> EnergyStatementResponse:
        """
        Retorna o balanço de energia geral com os dados de todos os subsistemas agrupados
        por data e hora de medição. Utiliza as medições no padrão antigo, medidas de hora em
        hora
        """
        async with self._session_maker() as session:
            statement = (
                select(HourlySubSystemProductionStatement)
                .filter(
                    HourlySubSystemProductionStatement.data.between(
                        data_inicial, data_final
                    )
                )
                .order_by(
                    HourlySubSystemProductionStatement.data,
                    HourlySubSystemProductionStatement.hora,
                )
                .limit(limit)
                .offset(offset)
            )
            result = (await session.execute(statement)).scalars().all()

        return EnergyStatementResponse(
            total_registros=len(result),
            data_inicial=data_inicial,
            data_final=data_final,
            dados=[
                HourlyEnergyStatement.model_validate(
                    energy_statement, from_attributes=True
                )
                for energy_statement in result
            ],
        )

    async def get_half_hourly_energy_statements(
        self,
        data_inicial: date,
        data_final: date,
        limit: int = 100,
        offset: int = 0,
    ) -> HalfHourlyEnergyStatementResponse:
        """
        Retorna o balanço de energia geral com os dados de todos os subsistemas. Utiliza
        as medições no padrão DESSEM, medidas a cada meia hora
        """
        async with self._session_maker() as session:
            statement = (
                select(HalfHourlySubSystemProductionStatement)
                .filter(HalfHourlySubSystemProductionStatement.data >= data_inicial)
                .filter(HalfHourlySubSystemProductionStatement.data <= data_final)
                .order_by(
                    HalfHourlySubSystemProductionStatement.data,
                    HalfHourlySubSystemProductionStatement.hora,
                )
                .limit(limit)
                .offset(offset)
            )
            result = (await session.execute(statement)).scalars().all()

            if not result:
                raise NotFoundException(
                    f"Nenhuma medição de energia semihorário disponível entre as datas {data_inicial.strftime('%d-%m-%Y')} e {data_final.strftime('%d-%m-%Y')}"
                )

            return HalfHourlyEnergyStatementResponse(
                total_registros=len(result),
                data_inicial=data_inicial,
                data_final=data_final,
                dados=[
                    HalfHourlyEnergyStatement.model_validate(
                        energy_statement, from_attributes=True
                    )
                    for energy_statement in result
                ],
            )
