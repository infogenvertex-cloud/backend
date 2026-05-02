from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class MemberCreate(BaseModel):
    name: str
    phone: str
    join_date: Optional[date] = None


class MemberUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None


class MemberResponse(BaseModel):
    id: int
    member_id: str
    name: str
    phone: str
    join_date: date

    model_config = ConfigDict(from_attributes=True)
