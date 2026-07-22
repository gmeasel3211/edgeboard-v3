from __future__ import annotations

from datetime import datetime, timezone
import httpx

from app.core.config import settings


class OddsAPIError(RuntimeError):
    pass


class OddsClient:
    base_url = "https://api.the-odds-api.com/v4"

    async def fetch_mlb_odds(self) -> tuple[list[dict], dict]:
        if not settings.odds_api_key:
            return [], {"configured": False, "remaining": None, "used": None}

        params = {
            "apiKey": settings.odds_api_key,
            "regions": settings.odds_regions,
            "markets": settings.odds_markets,
            "oddsFormat": "american",
            "dateFormat": "iso",
            "bookmakers": settings.odds_bookmakers,
        }
        async with httpx.AsyncClient(timeout=25) as client:
            response = await client.get(f"{self.base_url}/sports/baseball_mlb/odds", params=params)
        if response.status_code >= 400:
            raise OddsAPIError(f"Odds API returned {response.status_code}: {response.text[:300]}")
        usage = {
            "configured": True,
            "remaining": response.headers.get("x-requests-remaining"),
            "used": response.headers.get("x-requests-used"),
            "last": response.headers.get("x-requests-last"),
        }
        return response.json(), usage

    @staticmethod
    def normalize(events: list[dict]) -> list[dict]:
        rows: list[dict] = []
        allowed = settings.allowed_bookmakers
        captured_at = datetime.now(timezone.utc)
        for event in events:
            for bookmaker in event.get("bookmakers", []):
                if bookmaker.get("key") not in allowed:
                    continue
                book_updated = bookmaker.get("last_update")
                for market in bookmaker.get("markets", []):
                    market_key = market.get("key")
                    for outcome in market.get("outcomes", []):
                        rows.append({
                            "game_external_id": event["id"],
                            "home_team": event["home_team"],
                            "away_team": event["away_team"],
                            "starts_at": event["commence_time"],
                            "bookmaker": bookmaker["key"],
                            "market": market_key,
                            "selection": outcome["name"],
                            "american_odds": int(outcome["price"]),
                            "line": outcome.get("point"),
                            "bookmaker_updated_at": book_updated,
                            "captured_at": captured_at,
                        })
        return rows
