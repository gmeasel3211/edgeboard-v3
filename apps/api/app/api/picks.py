from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import subscriber_user
from app.core.database import get_db
from app.models import Pick, User
from app.schemas import PickOut
from app.services.mlb import demo_board

router = APIRouter(prefix="/picks", tags=["Picks"])


@router.get("/free")
def free_pick(db: Session = Depends(get_db)):
    pick = db.scalar(
        select(Pick).where(Pick.status == "pending").order_by(Pick.confidence.desc()).limit(1)
    )
    return pick or demo_board()[0]


@router.get("", response_model=list[PickOut])
def all_picks(db: Session = Depends(get_db), user: User = Depends(subscriber_user)):
    return list(db.scalars(
        select(Pick).where(Pick.status == "pending").order_by(
            Pick.confidence.desc(), Pick.starts_at.asc()
        )
    ).all())
