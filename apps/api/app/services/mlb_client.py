from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
import httpx

from app.core.config import settings


class MLBStatsClient:
    def __init__(self):
        self.base_url = settings.mlb_stats_base_url.rstrip("/")

    async def schedule(self, days_ahead: int = 3, days_back: int = 1) -> list[dict]:
        start = date.today() - timedelta(days=days_back)
        end = date.today() + timedelta(days=days_ahead)
        params = {
            "sportId": 1,
            "startDate": start.isoformat(),
            "endDate": end.isoformat(),
            "hydrate": "probablePitcher,venue,team,linescore",
        }
        async with httpx.AsyncClient(timeout=25) as client:
            response = await client.get(f"{self.base_url}/v1/schedule", params=params)
        response.raise_for_status()
        games = []
        for day in response.json().get("dates", []):
            games.extend(day.get("games", []))
        return games

    async def standings(self, season: int) -> list[dict]:
        params = {"leagueId": "103,104", "season": season, "standingsTypes": "regularSeason"}
        async with httpx.AsyncClient(timeout=25) as client:
            response = await client.get(f"{self.base_url}/v1/standings", params=params)
        response.raise_for_status()
        records = []
        for group in response.json().get("records", []):
            records.extend(group.get("teamRecords", []))
        return records

    async def pitcher_stats(self, person_id: int, season: int) -> dict | None:
        params = {"stats": "season", "group": "pitching", "season": season}
        async with httpx.AsyncClient(timeout=25) as client:
            response = await client.get(f"{self.base_url}/v1/people/{person_id}/stats", params=params)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        stats = response.json().get("stats", [])
        splits = stats[0].get("splits", []) if stats else []
        return splits[0].get("stat") if splits else None
