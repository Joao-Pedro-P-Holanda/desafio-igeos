from fastapi import HTTPException


class InvalidArgumentException(HTTPException):
    def __init__(self, detail: str, headers: dict[str, str] | None = None) -> None:
        super().__init__(422, detail, headers)
