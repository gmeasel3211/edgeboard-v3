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
    odds_regions: str = "us"
    odds_bookmakers: str = "fanduel,draftkings"
    odds_markets: str = "h2h,spreads,totals"

    mlb_stats_base_url: str = "https://statsapi.mlb.com/api"
    nws_base_url: str = "https://api.weather.gov"
    nws_user_agent: str = "EdgeBoard/3.0 (owner@example.com)"

    auto_refresh_enabled: bool = True
    odds_refresh_minutes: int = 10
    mlb_refresh_minutes: int = 30
    weather_refresh_minutes: int = 30

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

    @property
    def allowed_bookmakers(self) -> set[str]:
        return {x.strip() for x in self.odds_bookmakers.split(",") if x.strip()}


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
