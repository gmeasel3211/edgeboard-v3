from __future__ import annotations

from math import exp
from typing import Iterable

from app.services.stadiums import STADIUMS


def american_to_implied(odds: int) -> float:
    return 100 / (odds + 100) if odds > 0 else abs(odds) / (abs(odds) + 100)


def no_vig_probabilities(prices: list[int]) -> list[float]:
    raw = [american_to_implied(x) for x in prices]
    total = sum(raw) or 1
    return [x / total for x in raw]


def decimal_odds(american: int) -> float:
    return 1 + (american / 100 if american > 0 else 100 / abs(american))


def team_rating(snapshot) -> float:
    if not snapshot:
        return 0.0
    return max(-1.5, min(1.5, snapshot.run_differential_per_game / 2.0))


def pitcher_rating(snapshot) -> float:
    if not snapshot or snapshot.era is None:
        return 0.0
    era_component = (4.20 - snapshot.era) / 2.2
    whip_component = (1.30 - (snapshot.whip or 1.30)) / 0.50
    k_component = ((snapshot.strikeouts_per_9 or 8.2) - 8.2) / 6.0
    return max(-1.5, min(1.5, era_component * 0.55 + whip_component * 0.30 + k_component * 0.15))


def weather_run_adjustment(weather, home_team: str) -> float:
    stadium = STADIUMS.get(home_team, {})
    if stadium.get("roof"):
        return 0.0
    adjustment = 0.0
    if weather:
        if weather.temperature_f is not None:
            adjustment += (weather.temperature_f - 70) * 0.004
        if weather.wind_speed_mph is not None:
            adjustment += min(weather.wind_speed_mph, 25) * 0.008
        if weather.precipitation_probability is not None and weather.precipitation_probability >= 50:
            adjustment -= 0.08
    return max(-0.25, min(0.30, adjustment))


def projected_home_probability(home_team, away_team, home_pitcher, away_pitcher, market_home_prob: float) -> tuple[float, dict]:
    rating_diff = (
        team_rating(home_team) - team_rating(away_team)
        + pitcher_rating(home_pitcher) - pitcher_rating(away_pitcher)
        + 0.18
    )
    model_only = 1 / (1 + exp(-rating_diff))
    blended = market_home_prob * 0.58 + model_only * 0.42
    blended = max(0.08, min(0.92, blended))
    return blended, {
        "team_diff": round(team_rating(home_team) - team_rating(away_team), 3),
        "pitcher_diff": round(pitcher_rating(home_pitcher) - pitcher_rating(away_pitcher), 3),
        "home_field": 0.18,
        "market_weight": 0.58,
    }


def kelly_units(probability: float, american: int, fraction: float = 0.25, max_units: float = 2.0) -> float:
    dec = decimal_odds(american)
    b = dec - 1
    q = 1 - probability
    raw = ((b * probability) - q) / b if b > 0 else 0
    return round(max(0.0, min(max_units, raw * fraction * 10)), 2)


def evaluate_moneyline(selection: str, american: int, model_probability: float, market_probability: float) -> dict:
    edge = (model_probability - market_probability) * 100
    ev = (model_probability * decimal_odds(american) - 1) * 100
    confidence = max(45.0, min(95.0, 55 + edge * 2.5))
    return {
        "edge_percent": round(edge, 2),
        "expected_value_percent": round(ev, 2),
        "confidence": round(confidence, 1),
        "units": kelly_units(model_probability, american),
    }
