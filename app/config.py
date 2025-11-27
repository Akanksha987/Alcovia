from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Alcovia AI Content API"
    environment: Literal["dev", "prod"] = "dev"
    database_url: str = "sqlite+aiosqlite:///./app.db"
    secret_key: str = "change_me"
    access_token_expire_minutes: int = 30
    algorithm: str = "HS256"

    huggingface_api_key: str | None = None
    summarization_model: str = "facebook/bart-large-cnn"
    sentiment_model: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

