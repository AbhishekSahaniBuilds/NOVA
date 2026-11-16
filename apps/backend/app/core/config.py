from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Backend root directory
BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    # Application
    app_env: str = "development"
    debug: bool = True

    # Server
    host: str = "127.0.0.1"
    port: int = 8000

    # MongoDB
    mongodb_uri: str
    mongodb_database: str = "nova"

    # Groq AI
    groq_api_key: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
