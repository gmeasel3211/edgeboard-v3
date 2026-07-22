from __future__ import annotations

from datetime import datetime, timedelta, timezone
from math import exp
import hashlib


def american_to_probability(odds: int) -> float:
    if odds > 0:
        return 100 / (odds + 100)
    return abs(odds) / (abs(odds) + 100)


def deterministic_probability(label: str) -> float:
    digest = hashlib.sha256(label.encode()).hexdigest()
    raw = int(digest[:8], 16) / 0xFFFFFFFF
    return 0.51 + raw * 0.10


def demo_board() -> list[dict]:
    tomorrow = datetime.now(timezone.utc).replace(hour=23, minute=10, second=0, microsecond=0)
    games = [
        ("Boston Red Sox @ New York Yankees", "Yankees ML", -125, "DraftKings"),
        ("Los Angeles Dodgers @ San Diego Padres", "Dodgers ML", -118, "FanDuel"),
        ("Chicago Cubs @ St. Louis Cardinals", "Over 8.5", -105, "DraftKings"),
        ("Seattle Mariners @ Houston Astros", "Mariners +1.5", -140, "FanDuel"),
    ]
    output = []
    for index, (matchup, selection, odds, book) in enumerate(games):
        market_prob = american_to_probability(odds)
        model_prob = deterministic_probability(matchup + selection)
        edge = (model_prob - market_prob) * 100
        decimal_odds = 1 + (100 / abs(odds) if odds < 0 else odds / 100)
        ev = (model_prob * decimal_odds - 1) * 100
        confidence = min(99.0, max(50.0, 55 + edge * 3))
        units = round(max(0.25, min(2.0, edge / 5)), 2)
        output.append({
            "game_id": f"demo-{index+1}",
            "matchup": matchup,
            "market": "moneyline" if "ML" in selection else "spread_or_total",
            "selection": selection,
            "sportsbook": book,
            "american_odds": odds,
            "model_probability": round(model_prob, 4),
            "market_probability": round(market_prob, 4),
            "edge_percent": round(edge, 2),
            "expected_value_percent": round(ev, 2),
            "confidence": round(confidence, 1),
            "units": units,
            "explanation": "Model projection combines market price, baseline team strength, and conservative uncertainty controls.",
            "starts_at": tomorrow + timedelta(minutes=index * 35),
        })
    return output
