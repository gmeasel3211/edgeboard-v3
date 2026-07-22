from __future__ import annotations

import enum
from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class SubscriptionTier(str, enum.Enum):
    FREE = "free"
    PRO = "pro"
    ELITE = "elite"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    display_name: Mapped[str] = mapped_column(String(80), default="")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    subscription_tier: Mapped[SubscriptionTier] = mapped_column(
        Enum(SubscriptionTier), default=SubscriptionTier.FREE
    )
    stripe_customer_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    stripe_subscription_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    external_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    mlb_game_pk: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    home_team: Mapped[str] = mapped_column(String(100), index=True)
    away_team: Mapped[str] = mapped_column(String(100), index=True)
    home_team_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_team_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    venue_name: Mapped[str] = mapped_column(String(150), default="")
    venue_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    status: Mapped[str] = mapped_column(String(40), default="scheduled")
    home_probable_pitcher_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    home_probable_pitcher: Mapped[str] = mapped_column(String(120), default="")
    away_probable_pitcher_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_probable_pitcher: Mapped[str] = mapped_column(String(120), default="")
    home_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source_updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)


class OddsSnapshot(Base):
    __tablename__ = "odds_snapshots"
    __table_args__ = (
        UniqueConstraint(
            "game_external_id", "bookmaker", "market", "selection", "line", "captured_at",
            name="uq_odds_snapshot"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    game_external_id: Mapped[str] = mapped_column(String(100), index=True)
    bookmaker: Mapped[str] = mapped_column(String(50), index=True)
    market: Mapped[str] = mapped_column(String(30), index=True)
    selection: Mapped[str] = mapped_column(String(120), index=True)
    american_odds: Mapped[int] = mapped_column(Integer)
    line: Mapped[float | None] = mapped_column(Float, nullable=True)
    bookmaker_updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)


class TeamSnapshot(Base):
    __tablename__ = "team_snapshots"
    __table_args__ = (UniqueConstraint("team_id", "season", "captured_date", name="uq_team_snapshot"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_id: Mapped[int] = mapped_column(Integer, index=True)
    team_name: Mapped[str] = mapped_column(String(100))
    season: Mapped[int] = mapped_column(Integer)
    captured_date: Mapped[str] = mapped_column(String(10), index=True)
    wins: Mapped[int] = mapped_column(Integer, default=0)
    losses: Mapped[int] = mapped_column(Integer, default=0)
    runs_per_game: Mapped[float] = mapped_column(Float, default=0)
    runs_allowed_per_game: Mapped[float] = mapped_column(Float, default=0)
    run_differential_per_game: Mapped[float] = mapped_column(Float, default=0)
    raw: Mapped[dict] = mapped_column(JSON, default=dict)


class PitcherSnapshot(Base):
    __tablename__ = "pitcher_snapshots"
    __table_args__ = (UniqueConstraint("pitcher_id", "season", "captured_date", name="uq_pitcher_snapshot"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pitcher_id: Mapped[int] = mapped_column(Integer, index=True)
    pitcher_name: Mapped[str] = mapped_column(String(120))
    season: Mapped[int] = mapped_column(Integer)
    captured_date: Mapped[str] = mapped_column(String(10), index=True)
    era: Mapped[float | None] = mapped_column(Float, nullable=True)
    whip: Mapped[float | None] = mapped_column(Float, nullable=True)
    strikeouts_per_9: Mapped[float | None] = mapped_column(Float, nullable=True)
    walks_per_9: Mapped[float | None] = mapped_column(Float, nullable=True)
    innings_pitched: Mapped[float | None] = mapped_column(Float, nullable=True)
    raw: Mapped[dict] = mapped_column(JSON, default=dict)


class WeatherSnapshot(Base):
    __tablename__ = "weather_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    game_external_id: Mapped[str] = mapped_column(String(100), index=True)
    forecast_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    temperature_f: Mapped[float | None] = mapped_column(Float, nullable=True)
    wind_speed_mph: Mapped[float | None] = mapped_column(Float, nullable=True)
    wind_direction: Mapped[str] = mapped_column(String(20), default="")
    precipitation_probability: Mapped[float | None] = mapped_column(Float, nullable=True)
    short_forecast: Mapped[str] = mapped_column(String(160), default="")
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)


class Pick(Base):
    __tablename__ = "picks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sport: Mapped[str] = mapped_column(String(20), default="MLB", index=True)
    game_id: Mapped[str] = mapped_column(String(100), index=True)
    matchup: Mapped[str] = mapped_column(String(200))
    market: Mapped[str] = mapped_column(String(50))
    selection: Mapped[str] = mapped_column(String(100))
    sportsbook: Mapped[str] = mapped_column(String(50))
    american_odds: Mapped[int] = mapped_column(Integer)
    model_probability: Mapped[float] = mapped_column(Float)
    market_probability: Mapped[float] = mapped_column(Float)
    edge_percent: Mapped[float] = mapped_column(Float)
    expected_value_percent: Mapped[float] = mapped_column(Float)
    confidence: Mapped[float] = mapped_column(Float)
    units: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    result_units: Mapped[float | None] = mapped_column(Float, nullable=True)
    explanation: Mapped[str] = mapped_column(Text, default="")
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class RefreshRun(Base):
    __tablename__ = "refresh_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_name: Mapped[str] = mapped_column(String(60), index=True)
    status: Mapped[str] = mapped_column(String(20), index=True)
    details: Mapped[dict] = mapped_column(JSON, default=dict)
    error_message: Mapped[str] = mapped_column(Text, default="")
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
