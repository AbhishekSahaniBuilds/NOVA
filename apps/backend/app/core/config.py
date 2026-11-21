from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_env: str = "development"
    debug: bool = False
    host: str = "127.0.0.1"
    port: int = 8000

    mongodb_uri: str | None = None
    mongodb_database: str | None = None

    groq_api_key: str | None = None
    groq_model_primary: str = "openai/gpt-oss-120b"
    groq_model_fallback: str | None = "openai/gpt-oss-20b"

    gemini_api_key: str | None = None
    gemini_model_primary: str | None = None

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
