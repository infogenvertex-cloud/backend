from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.visitor import VisitorCreate, VisitorResponse
from app.services.visitor_service import (
    create_visitor,
    get_all_visitors,
    get_visitor_by_id,
    update_visitor,
    delete_visitor
)
from app.utils.deps import get_db, get_current_admin

router = APIRouter(prefix="/api/visitors", tags=["Visitors"])


@router.post("/", response_model=VisitorResponse)
def add_visitor(
    data: VisitorCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return create_visitor(db, data)


@router.get("/", response_model=List[VisitorResponse])
def list_visitors(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return get_all_visitors(db)


@router.get("/{visitor_id}", response_model=VisitorResponse)
def get_visitor(
    visitor_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    visitor = get_visitor_by_id(db, visitor_id)
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")
    return visitor


@router.put("/{visitor_id}", response_model=VisitorResponse)
def edit_visitor(
    visitor_id: int,
    data: VisitorCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    visitor = update_visitor(db, visitor_id, data)
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")
    return visitor


@router.delete("/{visitor_id}")
def remove_visitor(
    visitor_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    if not delete_visitor(db, visitor_id):
        raise HTTPException(status_code=404, detail="Visitor not found")
    return {"message": "Visitor deleted successfully"}
