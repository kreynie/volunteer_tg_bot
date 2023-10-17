from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

project_path = Path(__file__).resolve().parent


class Settings(BaseSettings):
    token: SecretStr
    db_url: str = f"sqlite+aiosqlite:///{project_path / 'db.sqlite3'}"
    db_echo: bool = False
    model_config = SettingsConfigDict(
        env_file=project_path / ".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
