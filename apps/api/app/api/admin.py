from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import admin_user
from app.core.database import get_db
from app.models import User
from app.services.pipeline import RefreshPipeline

router = APIRouter(prefix="/admin", tags=["Admin"])
pipeline = RefreshPipeline()


@router.post("/refresh/full")
async def refresh_full(_: User = Depends(admin_user)):
    return {"ok": True, "results": await pipeline.run_full()}


@router.post("/refresh/mlb")
async def refresh_mlb(_: User = Depends(admin_user)):
    return {"ok": True, "results": await pipeline.refresh_mlb()}


@router.post("/refresh/odds")
async def refresh_odds(_: User = Depends(admin_user)):
    result = await pipeline.refresh_odds()
    model = pipeline.rebuild_card()
    return {"ok": True, "results": result, "model": model}


@router.post("/refresh/weather")
async def refresh_weather(_: User = Depends(admin_user)):
    return {"ok": True, "results": await pipeline.refresh_weather()}


@router.post("/rebuild-card")
def rebuild_card(_: User = Depends(admin_user)):
    return {"ok": True, "results": pipeline.rebuild_card()}
