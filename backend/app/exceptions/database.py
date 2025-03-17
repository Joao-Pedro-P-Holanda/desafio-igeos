from fastapi import HTTPException
from http import HTTPStatus


class NotFoundException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(HTTPStatus.NOT_FOUND, detail)
