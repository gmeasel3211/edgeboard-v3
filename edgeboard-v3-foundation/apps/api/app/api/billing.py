from __future__ import annotations

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import current_user
from app.core.config import settings
from app.core.database import get_db
from app.models import SubscriptionTier, User
from app.schemas import CheckoutRequest

router = APIRouter(prefix="/billing", tags=["Billing"])


@router.post("/checkout")
def create_checkout(
    payload: CheckoutRequest,
    user: User = Depends(current_user),
):
    if payload.tier == SubscriptionTier.FREE:
        raise HTTPException(status_code=400, detail="Choose a paid tier")
    if not settings.stripe_secret_key:
        raise HTTPException(status_code=503, detail="Stripe is not configured")
    stripe.api_key = settings.stripe_secret_key
    price_id = (
        settings.stripe_pro_price_id
        if payload.tier == SubscriptionTier.PRO
        else settings.stripe_elite_price_id
    )
    if not price_id:
        raise HTTPException(status_code=503, detail="Stripe price is not configured")
    session = stripe.checkout.Session.create(
        mode="subscription",
        customer_email=user.email,
        line_items=[{"price": price_id, "quantity": 1}],
        success_url=f"{settings.frontend_url}/dashboard?checkout=success",
        cancel_url=f"{settings.frontend_url}/pricing?checkout=cancelled",
        metadata={"user_id": str(user.id), "tier": payload.tier.value},
    )
    return {"checkout_url": session.url}


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    if not settings.stripe_secret_key or not settings.stripe_webhook_secret:
        raise HTTPException(status_code=503, detail="Stripe is not configured")
    stripe.api_key = settings.stripe_secret_key
    body = await request.body()
    signature = request.headers.get("stripe-signature", "")
    try:
        event = stripe.Webhook.construct_event(body, signature, settings.stripe_webhook_secret)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid Stripe webhook") from exc

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        metadata = session.get("metadata") or {}
        user_id = int(metadata.get("user_id", 0))
        user = db.get(User, user_id)
        if user:
            user.subscription_tier = SubscriptionTier(metadata.get("tier", "pro"))
            user.stripe_customer_id = session.get("customer")
            user.stripe_subscription_id = session.get("subscription")
            db.commit()

    if event["type"] in {"customer.subscription.deleted", "customer.subscription.paused"}:
        subscription = event["data"]["object"]
        user = db.scalar(
            select(User).where(User.stripe_subscription_id == subscription.get("id"))
        )
        if user:
            user.subscription_tier = SubscriptionTier.FREE
            db.commit()

    return {"received": True}
