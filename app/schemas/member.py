from datetime import date
from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class MemberCreate(BaseModel):
    name: str
    phone: str
    join_date: Optional[date] = None


class MemberUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    join_date: Optional[date] = None


class MemberResponse(BaseModel):
    id: int
    member_id: str
    name: str
    phone: str
    join_date: date
    
    # Optional payment summary
    total_payments: Optional[float] = None
    last_payment_date: Optional[date] = None
    payment_count: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
