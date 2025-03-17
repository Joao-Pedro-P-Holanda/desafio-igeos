from pydantic import BaseModel


class SubSystem(BaseModel):
    id_subsistema: str
    nome_subsistema: str
