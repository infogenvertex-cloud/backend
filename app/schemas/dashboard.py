from __future__ import annotations

from typing import List

from pydantic import BaseModel

from app.schemas.payment import PaymentResponse


class DashboardStats(BaseModel):
    total_members: int
    active_members: int
    expiring_soon: int
    recent_payments: List[PaymentResponse]
