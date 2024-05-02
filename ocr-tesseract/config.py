from pathlib import Path
from typing import Any

from pydantic import RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(Path(__file__).parent.parent / ".env", ".env"),
        extra="ignore",
    )

    APP_DIR: Path = Path(__file__).parent
    BASE_DIR: Path = Path(__file__).parent.parent

    REDIS_USERNAME: str | None = None
    REDIS_PASSWORD: str | None = None
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    CORS_ORIGINS: list[str] = ["*"]
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str] = ["*"]

    APP_VERSION: str = "0.1.0"

    @property
    def REDIS_URL(self) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis",
            username=self.REDIS_USERNAME,
            password=self.REDIS_PASSWORD,
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
        )


settings = Config()  # type: ignore


app_configs: dict[str, Any] = {"title": "App API"}
