from typing import List

from pydantic import BaseModel

from app.schemas.payment import PaymentResponse


class DashboardStats(BaseModel):
    total_members: int
    active_members: int
    total_visitors: int
    total_payments: float
    monthly_revenue: float
    recent_payments: List[PaymentResponse]
    recent_visitors_count: int
