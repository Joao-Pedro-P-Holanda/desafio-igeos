from fastapi import HTTPException
from http import HTTPStatus


class UnauthenticatedException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(HTTPStatus.UNAUTHORIZED, detail=detail)


class ForbiddenException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(HTTPStatus.FORBIDDEN, detail=detail)
