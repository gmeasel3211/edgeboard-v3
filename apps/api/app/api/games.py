from __future__ import annotations

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import subscriber_user
from app.core.database import get_db
from app.models import Game, OddsSnapshot, Pick, User, WeatherSnapshot

router = APIRouter(prefix="/games", tags=["Games"])


@router.get("")
def games(db: Session = Depends(get_db), _: User = Depends(subscriber_user)):
    records = list(db.scalars(
        select(Game).where(Game.starts_at >= datetime.now(timezone.utc)).order_by(Game.starts_at.asc())
    ).all())
    output = []
    for game in records:
        latest_weather = db.scalar(select(WeatherSnapshot).where(
            WeatherSnapshot.game_external_id == game.external_id
        ).order_by(WeatherSnapshot.captured_at.desc()).limit(1))
        picks = list(db.scalars(select(Pick).where(Pick.game_id == game.external_id)).all())
        output.append({
            "id": game.external_id,
            "matchup": f"{game.away_team} @ {game.home_team}",
            "home_team": game.home_team,
            "away_team": game.away_team,
            "starts_at": game.starts_at,
            "venue": game.venue_name,
            "status": game.status,
            "probable_pitchers": {
                "away": game.away_probable_pitcher,
                "home": game.home_probable_pitcher,
            },
            "weather": None if not latest_weather else {
                "temperature_f": latest_weather.temperature_f,
                "wind_speed_mph": latest_weather.wind_speed_mph,
                "wind_direction": latest_weather.wind_direction,
                "precipitation_probability": latest_weather.precipitation_probability,
                "short_forecast": latest_weather.short_forecast,
            },
            "qualified_picks": len(picks),
        })
    return output


@router.get("/{game_id}")
def game_detail(game_id: str, db: Session = Depends(get_db), _: User = Depends(subscriber_user)):
    game = db.scalar(select(Game).where(Game.external_id == game_id))
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    odds = list(db.scalars(select(OddsSnapshot).where(
        OddsSnapshot.game_external_id == game_id
    ).order_by(OddsSnapshot.captured_at.desc()).limit(100)).all())
    picks = list(db.scalars(select(Pick).where(Pick.game_id == game_id)).all())
    return {
        "game": {
            "id": game.external_id,
            "matchup": f"{game.away_team} @ {game.home_team}",
            "home_team": game.home_team,
            "away_team": game.away_team,
            "starts_at": game.starts_at,
            "venue": game.venue_name,
            "status": game.status,
            "home_probable_pitcher": game.home_probable_pitcher,
            "away_probable_pitcher": game.away_probable_pitcher,
        },
        "odds": [{
            "bookmaker": x.bookmaker,
            "market": x.market,
            "selection": x.selection,
            "price": x.american_odds,
            "line": x.line,
            "captured_at": x.captured_at,
        } for x in odds],
        "picks": picks,
    }
