from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .config import config

engine = create_async_engine(config.DATABASE_URL)


def get_async_session() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine)
