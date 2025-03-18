from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from ..schemas import (
    HalfHourlySubSystemMarginalCostSchema,
    WeeklySubSystemMarginalCostSchema,
)

from ..models import HalfHourlySubSystemMarginalCost, WeeklySubSystemMarginalCost
from ..deps import AsyncSessionMakerDep


class CostCrud:
    def __init__(self, session_maker: AsyncSessionMakerDep):
        self._session_maker: async_sessionmaker[AsyncSession] = session_maker

    async def get_all_weekly(
        self, start_date: date, end_date: date, limit: int, offset: int
    ) -> list[WeeklySubSystemMarginalCostSchema]:
        async with self._session_maker() as session:
            statement = (
                select(WeeklySubSystemMarginalCost)
                .where(WeeklySubSystemMarginalCost.data.between(start_date, end_date))
                .limit(limit)
                .offset(offset)
            )
            result = await session.execute(statement)
            return [
                WeeklySubSystemMarginalCostSchema.model_validate(
                    row, from_attributes=True
                )
                for row in result.scalars().all()
            ]

    async def get_all_half_hourly(
        self, start_date: date, end_date: date, limit: int, offset: int
    ) -> list[HalfHourlySubSystemMarginalCostSchema]:
        async with self._session_maker() as session:
            statement = (
                select(HalfHourlySubSystemMarginalCost)
                .where(
                    HalfHourlySubSystemMarginalCost.data.between(start_date, end_date)
                )
                .limit(limit)
                .offset(offset)
            )
            result = await session.execute(statement)

            return [
                HalfHourlySubSystemMarginalCostSchema.model_validate(
                    row, from_attributes=True
                )
                for row in result
            ]
