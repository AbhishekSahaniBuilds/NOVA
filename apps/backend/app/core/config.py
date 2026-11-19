from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_env: str
    debug: bool
    host: str
    port: int

    mongodb_uri: str
    mongodb_database: str

    groq_api_key: str
    groq_model_primary: str
    groq_model_fallback: str

    gemini_api_key: str
    gemini_model_primary: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
