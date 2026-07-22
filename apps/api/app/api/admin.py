from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.api.deps import admin_user
from app.core.database import get_db
from app.models import Pick, User
from app.services.mlb import demo_board

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/refresh")
def refresh_board(
    db: Session = Depends(get_db),
    _: User = Depends(admin_user),
):
    db.execute(delete(Pick))
    for item in demo_board():
        db.add(Pick(sport="MLB", status="pending", **item))
    db.commit()
    return {"ok": True, "message": "MLB board refreshed", "count": 4}


@router.get("/health")
def admin_health(_: User = Depends(admin_user)):
    return {"api": "ok", "database": "ok", "model": "demo-ready"}
