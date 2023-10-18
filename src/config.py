from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

project_path = Path(__file__).resolve().parent


class DBSettings(BaseSettings):
    url: str = f"sqlite+aiosqlite:///{project_path / 'db.sqlite3'}"
    echo: bool = False


class Settings(BaseSettings):
    token: SecretStr
    db: DBSettings = DBSettings()
    model_config = SettingsConfigDict(
        env_file=project_path / ".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
