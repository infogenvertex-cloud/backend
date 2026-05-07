from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PaymentBase(BaseModel):
    amount: float
    plan: str  # "1_month", "3_months", "6_months", "1_year"
    notes: Optional[str] = None


class PaymentCreate(PaymentBase):
    member_id: int
    payment_date: Optional[datetime] = None


class PaymentUpdate(BaseModel):
    amount: Optional[float] = None
    plan: Optional[str] = None
    notes: Optional[str] = None
    payment_date: Optional[datetime] = None


class PaymentResponse(PaymentBase):
    id: int
    member_id: int
    payment_date: datetime
    
    # Optional member details
    member_name: Optional[str] = None
    member_code: Optional[str] = None
    member_phone: Optional[str] = None

    class Config:
        from_attributes = True
