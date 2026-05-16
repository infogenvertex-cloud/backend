from datetime import datetime
from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.payment import Payment
from app.models.member import Member
from app.schemas.payment import PaymentCreate, PaymentUpdate


def create_payment(db: Session, data: PaymentCreate) -> Payment:
    """Create a new payment record"""
    # Verify member exists
    member = db.query(Member).filter(Member.id == data.member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    payment_date = data.payment_date or datetime.utcnow()
    
    payment = Payment(
        member_id=data.member_id,
        amount=data.amount,
        plan=data.plan,
        notes=data.notes,
        payment_date=payment_date
    )
    db.add(payment)
    
    # Update member's last_payment_date to sort them to the top
    member.last_payment_date = payment_date
    
    db.commit()
    db.refresh(payment)
    return payment


def get_payment(db: Session, payment_id: int) -> Payment:
    """Get a single payment by ID"""
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


def get_payments(db: Session, skip: int = 0, limit: int = 100) -> List[Payment]:
    """Get all payments with pagination"""
    return db.query(Payment).order_by(Payment.payment_date.desc()).offset(skip).limit(limit).all()


def get_member_payments(db: Session, member_id: int) -> List[Payment]:
    """Get all payments for a specific member"""
    return db.query(Payment).filter(Payment.member_id == member_id).order_by(Payment.payment_date.desc()).all()


def update_payment(db: Session, payment_id: int, data: PaymentUpdate) -> Payment:
    """Update a payment record"""
    payment = get_payment(db, payment_id)
    
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(payment, field, value)
    
    db.commit()
    db.refresh(payment)
    return payment


def delete_payment(db: Session, payment_id: int):
    """Delete a payment record"""
    payment = get_payment(db, payment_id)
    db.delete(payment)
    db.commit()
