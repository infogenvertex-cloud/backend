from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.schemas.payment import PaymentCreate, PaymentUpdate, PaymentResponse
from app.services import payment_service
from app.utils.deps import get_db, get_current_admin
from app.utils.pagination import PaginatedResponse
from app.models.payment import Payment

router = APIRouter(prefix="/payments", tags=["Payments"], dependencies=[Depends(get_current_admin)])


def _enrich(payment):
    """Add member details to payment response"""
    resp = PaymentResponse(
        id=payment.id,
        member_id=payment.member_id,
        amount=payment.amount,
        plan=payment.plan,
        notes=payment.notes,
        payment_date=payment.payment_date,
    )
    if payment.member:
        resp.member_name = payment.member.name
        resp.member_code = payment.member.member_id
        resp.member_phone = payment.member.phone
    return resp


@router.post("/", response_model=PaymentResponse, status_code=201)
def create_payment(data: PaymentCreate, db: Session = Depends(get_db)):
    """Create a new payment record"""
    payment = payment_service.create_payment(db, data)
    return _enrich(payment)


@router.get("/", response_model=PaginatedResponse[PaymentResponse])
def list_payments(
    member_id: int = None,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """List all payments or filter by member_id with pagination"""
    skip = (page - 1) * page_size
    
    if member_id is not None:
        # Get payments for specific member
        payments = payment_service.get_member_payments(db, member_id)
        enriched = [_enrich(p) for p in payments]
        
        # Paginate in memory for member-specific queries
        total = len(enriched)
        paginated_items = enriched[skip:skip + page_size]
        
        return PaginatedResponse.create(
            items=paginated_items,
            total=total,
            page=page,
            page_size=page_size
        )
    else:
        # Get all payments with pagination
        payments = db.query(Payment).order_by(Payment.payment_date.desc()).offset(skip).limit(page_size).all()
        total = db.query(Payment).count()
        
        return PaginatedResponse.create(
            items=[_enrich(p) for p in payments],
            total=total,
            page=page,
            page_size=page_size
        )


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    """Get a single payment by ID"""
    payment = payment_service.get_payment(db, payment_id)
    return _enrich(payment)


@router.put("/{payment_id}", response_model=PaymentResponse)
def update_payment(payment_id: int, data: PaymentUpdate, db: Session = Depends(get_db)):
    """Update a payment record"""
    payment = payment_service.update_payment(db, payment_id, data)
    return _enrich(payment)


@router.delete("/{payment_id}", status_code=204)
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    """Delete a payment record"""
    payment_service.delete_payment(db, payment_id)
    return None
