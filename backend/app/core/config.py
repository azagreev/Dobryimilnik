from functools import lru_cache
from pathlib import Path
from typing import Literal
from urllib.parse import quote

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=None, extra="ignore")

    app_env: Literal["local", "prod"] = "local"
    app_name: str = "Dobryimilnik Backend"
    database_url: str = "postgresql+asyncpg://dobryimilnik:dobryimilnik@localhost:5432/dobryimilnik"
    redis_url: str = "redis://localhost:6379/0"
    meilisearch_url: str = "http://localhost:7700"
    keycloak_url: str = "http://localhost:8080"
    postgres_password_file: Path | None = Field(default=None)
    secret_key_file: Path | None = Field(default=None)

    @staticmethod
    def read_secret_file(path: Path | None) -> str | None:
        if path is None:
            return None
        return path.read_text(encoding="utf-8").strip()

    def postgres_password(self) -> str | None:
        return self.read_secret_file(self.postgres_password_file)

    def secret_key(self) -> str | None:
        return self.read_secret_file(self.secret_key_file)

    def sqlalchemy_database_url(self) -> str:
        password = self.postgres_password()
        if password is None or "@" not in self.database_url or "://" not in self.database_url:
            return self.database_url

        scheme, rest = self.database_url.split("://", 1)
        userinfo, hostinfo = rest.split("@", 1)
        if ":" in userinfo:
            return self.database_url
        return f"{scheme}://{userinfo}:{quote(password)}@{hostinfo}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
