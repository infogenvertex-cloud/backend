from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PaymentCreate(BaseModel):
    member_id: int
    amount: float


class PaymentResponse(BaseModel):
    id: int
    member_id: int
    member_code: Optional[str] = None
    member_name: Optional[str] = None
    member_phone: Optional[str] = None
    amount: float
    payment_date: datetime
    invoice_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
