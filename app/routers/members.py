from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.schemas.member import MemberCreate, MemberUpdate, MemberResponse
from app.services import member_service
from app.utils.deps import get_db, get_current_admin

router = APIRouter(prefix="/members", tags=["Members"], dependencies=[Depends(get_current_admin)])


@router.post("/", response_model=MemberResponse, status_code=201)
def create_member(data: MemberCreate, db: Session = Depends(get_db)):
    return member_service.create_member(db, data)


@router.get("/", response_model=List[MemberResponse])
def list_members(
    skip: int = 0, 
    limit: int = 100, 
    search: Optional[str] = Query(None, description="Search by name, phone, or member ID"),
    db: Session = Depends(get_db)
):
    if search:
        return member_service.search_members(db, search, skip, limit)
    return member_service.get_members(db, skip, limit)


@router.get("/{member_id:int}", response_model=MemberResponse)
def get_member(member_id: int, db: Session = Depends(get_db)):
    return member_service.get_member(db, member_id)


@router.put("/{member_id:int}", response_model=MemberResponse)
def update_member(member_id: int, data: MemberUpdate, db: Session = Depends(get_db)):
    return member_service.update_member(db, member_id, data)


@router.delete("/{member_id:int}", status_code=204)
def delete_member(member_id: int, db: Session = Depends(get_db)):
    member_service.delete_member(db, member_id)
