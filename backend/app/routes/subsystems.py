from datetime import date
from fastapi import APIRouter, Security

from ..crud.subsystem_crud import SubSystemCrud

from ..deps import AsyncSessionMakerDep

from ..schemas import SubSystem
from ..core.security import validate_token


router = APIRouter(dependencies=[Security(validate_token)])


@router.get("/")
async def list_subsystems(
    session_maker: AsyncSessionMakerDep,
) -> list[SubSystem]:
    """Retorna a lista de todos os subsistemas presentes"""
    crud = SubSystemCrud(session_maker)
    return await crud.get_all()


@router.get("/{id}")
async def get_subsystem(id: str, session_maker: AsyncSessionMakerDep):
    crud = SubSystemCrud(session_maker)
    return await crud.get(id)
