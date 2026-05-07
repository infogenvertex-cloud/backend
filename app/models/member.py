from datetime import date

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

from app.database import Base


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    member_id = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=False, unique=True)
    join_date = Column(Date, default=date.today)

    payments = relationship("Payment", back_populates="member", cascade="all, delete-orphan")
