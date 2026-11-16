from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Backend root directory
BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    # Application
    app_env: str
    debug: bool

    # Server
    host: str
    port: int

    # MongoDB
    mongodb_uri: str
    mongodb_database: str

    # Groq AI
    groq_api_key: str
    groq_model_primary: str = "openai/gpt-oss-120b"
    groq_model_fallback: str = "your_fallback_model_id"

    # Google AI Studio
    gemini_api_key: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
