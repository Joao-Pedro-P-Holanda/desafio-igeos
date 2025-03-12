from typing import Annotated
from fastapi import APIRouter, Form
from pydantic import EmailStr

# TODO: implement authentication either with auth0 or with native fastapi security

router = APIRouter()


@router.post("/criar-conta")
def create_user(): ...


@router.post("/login")
def create_user_session(): ...


# Note: if Auth0 is used this routes won't be implemented by hand


@router.post("/alterar-senha")
def request_password_reset(email: Annotated[EmailStr, Form()]):
    """
    Inicia uma mudança de senha que deve ser confirmada pelo email
    """

    ...


@router.post("/verificar-codigo-redefinicao")
def validate_password_reset_code(code: Annotated[str, Form()]):
    """
    Valida o código de mudança de senha para prosseguir com a mudança
    """
    ...


@router.post("/nova-senha")
def update_password(new_password: Annotated[str, Form()]):
    """
    Realiza a mudança da senha do usuário após o código ser validado
    """
    ...
