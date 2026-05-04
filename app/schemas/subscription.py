from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class SubscriptionCreate(BaseModel):
    member_id: int
    plan: str
    start_date: date
    amount: float  # Payment amount merged
    payment_date: Optional[date] = None  # Optional payment date (defaults to today if not provided)
    
    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v):
        if v is None or v <= 0:
            raise ValueError('Amount must be greater than 0')
        return v


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
    # Payment fields merged (Optional for backward compatibility with old records)
    amount: Optional[float] = None
    payment_date: Optional[datetime] = None
    invoice_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
