from __future__ import annotations

from datetime import date
import logging

from fastapi import HTTPException
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.member import Member
from app.schemas.member import MemberCreate, MemberUpdate

logger = logging.getLogger(__name__)


def _generate_member_id(db: Session) -> str:
    last = db.query(func.max(Member.id)).scalar()
    next_num = (last or 0) + 1
    return f"GYM-{next_num:04d}"


def create_member(db: Session, data: MemberCreate) -> Member:
    logger.info("🏗️ Member service: create_member called")
    logger.info(f"📋 Input data: {data}")
    
    member_id = _generate_member_id(db)
    logger.info(f"🆔 Generated member_id: {member_id}")
    
    # Handle join_date
    final_join_date = data.join_date or date.today()
    logger.info(f"📅 Join date processing: original={data.join_date}, final={final_join_date}")
    
    member = Member(
        member_id=member_id,
        name=data.name,
        phone=data.phone,
        join_date=final_join_date,
    )
    
    logger.info(f"👤 Creating member object: {member.__dict__}")
    
    try:
        db.add(member)
        db.commit()
        db.refresh(member)
        logger.info(f"✅ Member saved to database: {member.__dict__}")
        return member
    except Exception as e:
        logger.error(f"❌ Database error: {str(e)}")
        db.rollback()
        raise


def get_members(db: Session, skip: int = 0, limit: int = 100) -> list[Member]:
    return db.query(Member).offset(skip).limit(limit).all()


def search_members(db: Session, query: str, skip: int = 0, limit: int = 100) -> list[Member]:
    """
    Search members by name, phone, or member_id.
    Uses indexed columns for efficient searching.
    """
    if not query or len(query.strip()) == 0:
        return get_members(db, skip, limit)
    
    search_term = f"%{query.strip()}%"
    
    # Search across name, phone, and member_id using OR condition
    # This uses database indexes for efficient searching
    return (
        db.query(Member)
        .filter(
            or_(
                Member.name.ilike(search_term),
                Member.phone.ilike(search_term),
                Member.member_id.ilike(search_term)
            )
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_member(db: Session, member_id: int) -> Member:
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


def update_member(db: Session, member_id: int, data: MemberUpdate) -> Member:
    logger.info(f"🔄 Updating member {member_id} in service")
    logger.info(f"📋 Update data received: {data}")
    logger.info(f"🔍 Update data dict: {data.model_dump()}")
    logger.info(f"🔍 Update data (exclude_unset): {data.model_dump(exclude_unset=True)}")
    
    member = get_member(db, member_id)
    logger.info(f"👤 Current member before update: {member.__dict__}")
    
    update_data = data.model_dump(exclude_unset=True)
    logger.info(f"📝 Fields to update: {update_data}")
    
    for key, value in update_data.items():
        old_value = getattr(member, key, None)
        setattr(member, key, value)
        logger.info(f"🔄 Updated {key}: {old_value} → {value}")
    
    logger.info(f"👤 Member after setattr: {member.__dict__}")
    
    try:
        db.commit()
        logger.info("✅ Database commit successful")
        db.refresh(member)
        logger.info(f"👤 Member after refresh: {member.__dict__}")
        return member
    except Exception as e:
        logger.error(f"❌ Database commit failed: {str(e)}")
        db.rollback()
        raise


def delete_member(db: Session, member_id: int) -> None:
    member = get_member(db, member_id)
    db.delete(member)
    db.commit()
