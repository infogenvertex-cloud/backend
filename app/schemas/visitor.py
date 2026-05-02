from datetime import datetime
from pydantic import BaseModel, field_validator
import re


class VisitorCreate(BaseModel):
    name: str
    mobile: str

    @field_validator('mobile')
    @classmethod
    def validate_mobile(cls, v):
        # Remove spaces, dashes, and parentheses
        cleaned = re.sub(r'[\s\-\(\)]', '', v)
        
        # Check if it contains only digits and optional + at start
        if not re.match(r'^\+?\d{10,15}$', cleaned):
            raise ValueError('Mobile number must be 10-15 digits, optionally starting with +')
        
        return cleaned

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        return v.strip()


class VisitorResponse(BaseModel):
    id: int
    name: str
    mobile: str
    visited_at: datetime

    class Config:
        from_attributes = True
