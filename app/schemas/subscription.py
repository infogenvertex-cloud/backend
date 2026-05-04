from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SubscriptionCreate(BaseModel):
    member_id: int
    plan: str
    start_date: date
    amount: float  # Payment amount merged


class SubscriptionUpdate(BaseModel):
    plan: Optional[str] = None
    start_date: Optional[date] = None
    status: Optional[str] = None


class SubscriptionResponse(BaseModel):
    id: int
    member_id: int
    member_code: Optional[str] = None
    member_name: Optional[str] = None
    member_phone: Optional[str] = None
    plan: str
    start_date: date
    end_date: date
    status: str
    # Payment fields merged
    amount: float
    payment_date: datetime
    invoice_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
