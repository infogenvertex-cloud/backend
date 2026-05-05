from __future__ import annotations

from typing import List

from pydantic import BaseModel

from app.schemas.subscription import SubscriptionResponse  # Use SubscriptionResponse instead of PaymentResponse


class DashboardStats(BaseModel):
    total_members: int
    active_members: int
    expiring_soon: int
    recent_payments: List[SubscriptionResponse]  # Changed from PaymentResponse to SubscriptionResponse
