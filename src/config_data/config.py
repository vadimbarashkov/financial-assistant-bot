import pathlib

from pydantic_settings import BaseSettings
from pydantic import MongoDsn, RedisDsn, field_validator
from pydantic_core.core_schema import ValidationInfo


class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_IDS: list[int]

    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_PATH: str

    DATABASE_URL: MongoDsn | None = None

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_database_connection(cls, value: str | None, info: ValidationInfo) -> str | MongoDsn:
        if isinstance(value, str):
            return value

        return MongoDsn.build(
            scheme="mongodb",
            username=info.data.get("DATABASE_USERNAME"),
            password=info.data.get("DATABASE_PASSWORD"),
            host=info.data.get("DATABASE_HOST"),
            port=info.data.get("DATABASE_PORT"),
            path=info.data.get("DATABASE_PATH")
        )

    REDIS_USERNAME: str
    REDIS_PASSWORD: str
    REDIS_HOST: str
    REDIS_PORT: int

    REDIS_URL: RedisDsn | None = None

    @field_validator("REDIS_URL", mode="before")
    @classmethod
    def assemble_redis_connection(cls, value: str | None, info: ValidationInfo) -> str | RedisDsn:
        if isinstance(value, str):
            return value

        return RedisDsn.build(
            scheme="redis",
            username=info.data.get("REDIS_USERNAME"),
            password=info.data.get("REDIS_PASSWORD"),
            host=info.data.get("REDIS_HOST"),
            port=info.data.get("REDIS_PORT")
        )

    class Config:
        env_file: str = f"{pathlib.Path(__file__).parents[2]}/.env"


settings: Settings = Settings()
