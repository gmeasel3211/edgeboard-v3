from __future__ import annotations

from datetime import datetime, timezone
import re
import httpx

from app.core.config import settings


def parse_wind_speed(value: str | None) -> float | None:
    if not value:
        return None
    numbers = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", value)]
    return sum(numbers) / len(numbers) if numbers else None


class NWSClient:
    def __init__(self):
        self.headers = {
            "User-Agent": settings.nws_user_agent,
            "Accept": "application/geo+json",
        }

    async def hourly_forecast(self, latitude: float, longitude: float) -> list[dict]:
        async with httpx.AsyncClient(timeout=25, headers=self.headers) as client:
            point = await client.get(f"{settings.nws_base_url}/points/{latitude:.4f},{longitude:.4f}")
            point.raise_for_status()
            hourly_url = point.json()["properties"]["forecastHourly"]
            forecast = await client.get(hourly_url)
            forecast.raise_for_status()
            return forecast.json()["properties"]["periods"]

    @staticmethod
    def closest_period(periods: list[dict], starts_at: datetime) -> dict | None:
        if starts_at.tzinfo is None:
            starts_at = starts_at.replace(tzinfo=timezone.utc)
        candidates = []
        for period in periods:
            try:
                dt = datetime.fromisoformat(period["startTime"])
                candidates.append((abs((dt - starts_at).total_seconds()), period))
            except (KeyError, ValueError):
                continue
        return min(candidates, key=lambda x: x[0])[1] if candidates else None
