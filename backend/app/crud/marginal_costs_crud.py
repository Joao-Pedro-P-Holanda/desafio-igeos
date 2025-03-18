from datetime import date
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.exceptions.database import NotFoundException

from ..schemas import (
    HalfHourlySubSystemMarginalCostResponse,
    HalfHourlySubSystemMarginalCostSchema,
    WeeklySubSystemMarginalCostResponse,
    WeeklySubSystemMarginalCostSchema,
)

from ..models import HalfHourlySubSystemMarginalCost, WeeklySubSystemMarginalCost
from ..deps import AsyncSessionMakerDep


class CostCrud:
    def __init__(self, session_maker: AsyncSessionMakerDep):
        self._session_maker: async_sessionmaker[AsyncSession] = session_maker

    async def get_all_weekly(
        self, start_date: date, end_date: date, limit: int, offset: int
    ) -> WeeklySubSystemMarginalCostResponse:
        async with self._session_maker() as session:
            count_statement = select(func.count(WeeklySubSystemMarginalCost.id)).where(
                WeeklySubSystemMarginalCost.data.between(start_date, end_date)
            )

            list_statement = (
                select(WeeklySubSystemMarginalCost)
                .where(WeeklySubSystemMarginalCost.data.between(start_date, end_date))
                .limit(limit)
                .offset(offset)
            )
            result = (await session.execute(list_statement)).scalars().all()

            if not result:
                raise NotFoundException(
                    f"Nenhuma medição de custo marginal de operação semanal disponível entre as datas {start_date.strftime('%d-%m-%Y')} e {end_date.strftime('%d-%m-%Y')}"
                )

            count_result = (await session.execute(count_statement)).scalar_one()

            return WeeklySubSystemMarginalCostResponse(
                total_registros=count_result,
                data_inicial=start_date,
                data_final=end_date,
                dados=[
                    WeeklySubSystemMarginalCostSchema.model_validate(
                        row, from_attributes=True
                    )
                    for row in result
                ],
            )

    async def get_all_half_hourly(
        self, start_date: date, end_date: date, limit: int, offset: int
    ) -> HalfHourlySubSystemMarginalCostResponse:
        async with self._session_maker() as session:
            count_statement = select(
                func.count(HalfHourlySubSystemMarginalCost.id)
            ).where(HalfHourlySubSystemMarginalCost.data.between(start_date, end_date))

            list_statement = (
                select(HalfHourlySubSystemMarginalCost)
                .where(
                    HalfHourlySubSystemMarginalCost.data.between(start_date, end_date)
                )
                .limit(limit)
                .offset(offset)
            )
            result = (await session.execute(list_statement)).scalars().all()

            if not result:
                raise NotFoundException(
                    f"Nenhuma medição de custo marginal de operação semanal disponível entre as datas {start_date.strftime('%d-%m-%Y')} e {end_date.strftime('%d-%m-%Y')}"
                )

            count_result = (await session.execute(count_statement)).scalar_one()

            return HalfHourlySubSystemMarginalCostResponse(
                total_registros=count_result,
                data_inicial=start_date,
                data_final=end_date,
                dados=[
                    HalfHourlySubSystemMarginalCostSchema.model_validate(
                        row, from_attributes=True
                    )
                    for row in result
                ],
            )
