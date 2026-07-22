from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import current_user, subscriber_user
from app.core.database import get_db
from app.models import Pick, User
from app.schemas import PickOut
from app.services.mlb import demo_board

router = APIRouter(prefix="/picks", tags=["Picks"])


@router.get("/free")
def free_pick():
    return demo_board()[0]


@router.get("", response_model=list[PickOut])
def all_picks(
    db: Session = Depends(get_db),
    user: User = Depends(subscriber_user),
):
    picks = list(db.scalars(select(Pick).order_by(Pick.starts_at.asc())).all())
    if picks:
        return picks
    demo = demo_board()
    return [
        Pick(id=i + 1, sport="MLB", status="pending", **item)
        for i, item in enumerate(demo)
    ]
