from sqlalchemy import func, select
from ..deps import AsyncSessionMakerDep
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from ..exceptions.database import NotFoundException
from ..models import SubSystem as SubSystemTable
from ..schemas import SubSystem


class SubSystemCrud:
    def __init__(self, session_maker: AsyncSessionMakerDep):
        self._session_maker: async_sessionmaker[AsyncSession] = session_maker

    async def get(self, id: str) -> SubSystem:
        async with self._session_maker() as session:
            result = await session.get(SubSystemTable, id)
            if not result:
                raise NotFoundException(
                    detail=f"Nenhum subsistema encontrado com o id '{id}'"
                )
            return SubSystem.model_validate(result, from_attributes=True)

    async def get_all(self) -> list[SubSystem]:
        async with self._session_maker() as session:
            list_statement = select(SubSystemTable).order_by(
                SubSystemTable.nome_subsistema
            )
            result = (await session.execute(list_statement)).scalars().all()
            subsystems = [
                SubSystem.model_validate(model, from_attributes=True)
                for model in result
            ]

            if not result:
                raise NotFoundException(detail="Nenhum subsistema encontrado")

            return subsystems
