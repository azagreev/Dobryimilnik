from pathlib import Path

import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_settings_accept_local_and_prod(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "local")
    assert Settings().app_env == "local"

    monkeypatch.setenv("APP_ENV", "prod")
    assert Settings().app_env == "prod"


def test_settings_reject_unknown_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "staging")

    with pytest.raises(ValidationError):
        Settings()


def test_settings_do_not_require_committed_secret_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("POSTGRES_PASSWORD_FILE", raising=False)
    monkeypatch.delenv("SECRET_KEY_FILE", raising=False)

    settings = Settings()

    assert settings.postgres_password() is None
    assert settings.secret_key() is None


def test_settings_read_secret_file(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    secret_file = tmp_path / "secret.txt"
    secret_file.write_text("local-secret\n", encoding="utf-8")
    monkeypatch.setenv("SECRET_KEY_FILE", str(secret_file))

    settings = Settings()

    assert settings.secret_key() == "local-secret"


def test_settings_inject_postgres_password_from_file(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    password_file = tmp_path / "postgres_password.txt"
    password_file.write_text("local password/with slash\n", encoding="utf-8")
    monkeypatch.setenv(
        "DATABASE_URL", "postgresql+asyncpg://dobryimilnik@postgres:5432/dobryimilnik"
    )
    monkeypatch.setenv("POSTGRES_PASSWORD_FILE", str(password_file))

    settings = Settings()

    assert (
        settings.sqlalchemy_database_url()
        == "postgresql+asyncpg://dobryimilnik:local%20password%2Fwith%20slash@postgres:5432/dobryimilnik"
    )
