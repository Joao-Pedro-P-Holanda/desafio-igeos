from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    DATABASE_URL: str

    AUTH0_DOMAIN: str
    AUTH0_ISSUER: str
    AUTH0_AUDIENCE: str
    AUTH0_ALGORITHM: str


config = Config()  # type:ignore
