from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models import SubscriptionTier


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    display_name: str = Field(default="", max_length=80)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    display_name: str
    is_admin: bool
    subscription_tier: SubscriptionTier

    model_config = ConfigDict(from_attributes=True)


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class PickOut(BaseModel):
    id: int
    sport: str
    matchup: str
    market: str
    selection: str
    sportsbook: str
    american_odds: int
    model_probability: float
    edge_percent: float
    expected_value_percent: float
    confidence: float
    units: float
    status: str
    explanation: str
    starts_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CheckoutRequest(BaseModel):
    tier: SubscriptionTier
