from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
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
from app.utils.pagination import PaginatedResponse
from app.models.visitor import Visitor

router = APIRouter(prefix="/visitors", tags=["Visitors"])


@router.post("/", response_model=VisitorResponse)
def add_visitor(
    data: VisitorCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return create_visitor(db, data)


@router.get("/", response_model=PaginatedResponse[VisitorResponse])
def list_visitors(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    skip = (page - 1) * page_size
    
    # Get paginated visitors
    visitors = db.query(Visitor).order_by(Visitor.visited_at.desc()).offset(skip).limit(page_size).all()
    
    # Get total count
    total = db.query(Visitor).count()
    
    return PaginatedResponse.create(
        items=[VisitorResponse.model_validate(v, from_attributes=True) for v in visitors],
        total=total,
        page=page,
        page_size=page_size
    )


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
