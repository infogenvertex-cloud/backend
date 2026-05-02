from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from app.schemas.payment import PaymentCreate, PaymentResponse
from app.services import payment_service
from app.services.whatsapp_service import send_invoice
from app.utils.deps import get_db, get_current_admin

router = APIRouter(prefix="/api/payments", tags=["Payments"], dependencies=[Depends(get_current_admin)])


def _enrich(payment):
    """Add member details from the related member."""
    resp = PaymentResponse.model_validate(payment)
    if payment.member:
        resp.member_code = payment.member.member_id
        resp.member_name = payment.member.name
        resp.member_phone = payment.member.phone
    return resp


@router.post("/", response_model=PaymentResponse, status_code=201)
def create_payment(data: PaymentCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    payment, member = payment_service.create_payment(db, data.member_id, data.amount)
    background_tasks.add_task(send_invoice, member.phone, payment.invoice_url, member.name)
    resp = _enrich(payment)
    return resp


@router.get("/", response_model=List[PaymentResponse])
def list_payments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    payments = payment_service.get_payments(db, skip, limit)
    return [_enrich(p) for p in payments]


@router.get("/member/{member_id}", response_model=List[PaymentResponse])
def get_member_payments(member_id: int, db: Session = Depends(get_db)):
    payments = payment_service.get_member_payments(db, member_id)
    return [_enrich(p) for p in payments]
