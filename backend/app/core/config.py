from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import re


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    DATABASE_URL: SecretStr

    @field_validator("DATABASE_URL")
    def specify_database_engine(cls, v: SecretStr):
        if "://" not in v.get_secret_value():
            raise ValueError("Protocol not specified for database")

        protocol_splitted = v.get_secret_value().split("://")
        if not re.match("\w+\+\w+", protocol_splitted[0]):
            raise ValueError(
                "Url should specify engine in the format <protocol>+<engine>://"
            )
        return v

    AUTH0_DOMAIN: str
    AUTH0_ISSUER: str
    AUTH0_AUDIENCE: str
    AUTH0_ALGORITHM: str


config = Config()  # type:ignore
