from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models import RefreshRun

router = APIRouter(prefix="/system", tags=["System"])


@router.get("/status")
def status(db: Session = Depends(get_db)):
    runs = list(db.scalars(
        select(RefreshRun).order_by(RefreshRun.started_at.desc()).limit(10)
    ).all())
    return {
        "live_odds_configured": bool(settings.odds_api_key),
        "auto_refresh_enabled": settings.auto_refresh_enabled,
        "allowed_bookmakers": sorted(settings.allowed_bookmakers),
        "refresh_interval_minutes": settings.odds_refresh_minutes,
        "recent_runs": [{
            "job": x.job_name,
            "status": x.status,
            "details": x.details,
            "error": x.error_message,
            "started_at": x.started_at,
            "finished_at": x.finished_at,
        } for x in runs],
    }
