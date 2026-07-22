from __future__ import annotations

from functools import lru_cache
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "EdgeBoard API"
    app_env: str = "development"
    secret_key: str = "development-only-secret-change-me"
    database_url: str = "sqlite:///./edgeboard.sqlite3"
    cors_origins: list[str] | str = ["http://localhost:3000"]
    frontend_url: str = "http://localhost:3000"
    admin_email: str = "owner@example.com"
    odds_api_key: str = ""
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    stripe_pro_price_id: str = ""
    stripe_elite_price_id: str = ""
    access_token_minutes: int = 60 * 24 * 7

    model_config = SettingsConfigDict(env_file="../../.env", extra="ignore")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors(cls, value):
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
