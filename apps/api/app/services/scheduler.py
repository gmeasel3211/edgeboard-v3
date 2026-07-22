from __future__ import annotations

import logging
from datetime import datetime, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.core.config import settings
from app.services.pipeline import RefreshPipeline

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler(timezone="UTC")
pipeline = RefreshPipeline()


async def safe_full_refresh():
    try:
        await pipeline.run_full()
    except Exception:
        logger.exception("Scheduled EdgeBoard refresh failed")


def start_scheduler() -> None:
    if not settings.auto_refresh_enabled or scheduler.running:
        return
    scheduler.add_job(
        safe_full_refresh,
        "interval",
        minutes=max(5, settings.odds_refresh_minutes),
        id="full-refresh",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
        next_run_time=datetime.now(timezone.utc),
    )
    scheduler.start()


def stop_scheduler() -> None:
    if scheduler.running:
        scheduler.shutdown(wait=False)
