from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .core.database import get_async_session

AsyncSessionMakerDep = Annotated[
    async_sessionmaker[AsyncSession], Depends(get_async_session)
]
