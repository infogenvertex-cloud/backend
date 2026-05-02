from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from app.database import Base


class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    mobile = Column(String(15), nullable=False)
    visited_at = Column(DateTime, default=datetime.utcnow)
