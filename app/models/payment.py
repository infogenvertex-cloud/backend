from datetime import datetime

from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Payment(Base):
    """Simple payment record for members"""
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    plan = Column(String(50), nullable=False)  # e.g., "1_month", "3_months", "6_months", "1_year"
    notes = Column(String(200), nullable=True)

    member = relationship("Member", back_populates="payments")
