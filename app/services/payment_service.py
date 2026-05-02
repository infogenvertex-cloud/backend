from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.payment import Payment
from app.models.member import Member
from app.services.invoice_service import generate_invoice


def create_payment(db: Session, member_id: int, amount: float) -> Payment:
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    payment = Payment(member_id=member_id, amount=amount)
    db.add(payment)
    db.commit()
    db.refresh(payment)

    invoice_url = generate_invoice(
        payment_id=payment.id,
        member_code=member.member_id,
        member_name=member.name,
        member_phone=member.phone,
        amount=payment.amount,
        payment_date=payment.payment_date,
    )
    payment.invoice_url = invoice_url
    db.commit()
    db.refresh(payment)

    return payment, member


def get_payments(db: Session, skip: int = 0, limit: int = 100) -> list[Payment]:
    return db.query(Payment).order_by(Payment.payment_date.desc()).offset(skip).limit(limit).all()


def get_member_payments(db: Session, member_id: int) -> list[Payment]:
    return db.query(Payment).filter(Payment.member_id == member_id).order_by(Payment.payment_date.desc()).all()
