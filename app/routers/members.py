from typing import List, Optional
import logging

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.models.admin import Admin
from app.schemas.member import MemberCreate, MemberUpdate, MemberResponse
from app.services import member_service
from app.utils.deps import get_db, get_current_admin
from app.utils.pagination import PaginatedResponse

router = APIRouter(prefix="/members", tags=["Members"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=MemberResponse, status_code=201)
def create_member(
    data: MemberCreate,
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    logger.info("🚀 Creating new member - Backend API called")
    logger.info(f"📤 Received data: {data}")
    logger.info(f"🔍 Join date details: {data.join_date} (type: {type(data.join_date)})")
    
    try:
        result = member_service.create_member(db, data)
        logger.info(f"✅ Member created successfully: {result.member_id}")
        logger.info(f"📋 Created member details: ID={result.id}, join_date={result.join_date}")
        return result
    except Exception as e:
        logger.error(f"❌ Error creating member: {str(e)}")
        logger.error(f"📋 Failed data: {data}")
        raise


@router.get("/", response_model=PaginatedResponse[MemberResponse])
def list_members(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by name, phone, or member ID"),
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    skip = (page - 1) * page_size
    
    if search:
        members = member_service.search_members(db, search, skip, page_size)
        total = len(member_service.search_members(db, search, 0, 10000))  # Get total count
    else:
        members = member_service.get_members(db, skip, page_size)
        total = db.query(member_service.Member).count()
    
    return PaginatedResponse.create(
        items=members,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{member_id:int}", response_model=MemberResponse)
def get_member(
    member_id: int,
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    return member_service.get_member(db, member_id)


@router.put("/{member_id:int}", response_model=MemberResponse)
def update_member(
    member_id: int,
    data: MemberUpdate,
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    logger.info(f"🔄 Updating member {member_id} - Backend API called")
    logger.info(f"📤 Received update data: {data}")
    logger.info(f"📤 Data model_dump: {data.model_dump()}")
    logger.info(f"📤 Data model_dump(exclude_unset=True): {data.model_dump(exclude_unset=True)}")
    logger.info(f"🔍 Join date details: {data.join_date} (type: {type(data.join_date)})")
    logger.info(f"🔍 Name: {data.name}, Phone: {data.phone}")
    
    try:
        result = member_service.update_member(db, member_id, data)
        logger.info(f"✅ Member updated successfully: {result.member_id}")
        logger.info(f"📋 Updated member details: ID={result.id}, name={result.name}, phone={result.phone}, join_date={result.join_date}")
        return result
    except Exception as e:
        logger.error(f"❌ Error updating member {member_id}: {str(e)}")
        logger.error(f"📋 Failed data: {data}")
        import traceback
        logger.error(f"📋 Traceback: {traceback.format_exc()}")
        raise


@router.delete("/{member_id:int}", status_code=204)
def delete_member(
    member_id: int,
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    member_service.delete_member(db, member_id)
