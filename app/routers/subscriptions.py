from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import BytesIO

from app.schemas.subscription import SubscriptionCreate, SubscriptionUpdate, SubscriptionResponse
from app.services import subscription_service
from app.services.invoice_service import generate_invoice_pdf
from app.utils.deps import get_db, get_current_admin

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"], dependencies=[Depends(get_current_admin)])


def _enrich(sub):
    """Add member details from the related member."""
    # Explicit mapping to ensure all fields are properly loaded (fixes undefined issue)
    resp = SubscriptionResponse(
        id=sub.id,
        member_id=sub.member_id,
        plan=sub.plan,
        start_date=sub.start_date,
        end_date=sub.end_date,
        status=sub.status,
        # Explicit mapping for payment fields (fixes undefined values)
        amount=sub.amount,
        payment_date=sub.payment_date,
        invoice_url=sub.invoice_url,
    )
    if sub.member:
        resp.member_code = sub.member.member_id
        resp.member_name = sub.member.name
        resp.member_phone = sub.member.phone
    return resp


@router.post("/", response_model=SubscriptionResponse, status_code=201)
def create_subscription(data: SubscriptionCreate, db: Session = Depends(get_db)):
    """Create subscription with payment."""
    subscription, member = subscription_service.create_subscription(db, data)
    return _enrich(subscription)


@router.get("/", response_model=List[SubscriptionResponse])
def list_subscriptions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    subs = subscription_service.get_subscriptions(db, skip, limit)
    return [_enrich(s) for s in subs]


@router.get("/member/{member_id}", response_model=List[SubscriptionResponse])
def get_member_subscriptions(member_id: int, db: Session = Depends(get_db)):
    subs = subscription_service.get_member_subscriptions(db, member_id)
    return [_enrich(s) for s in subs]


@router.get("/{subscription_id}", response_model=SubscriptionResponse)
def get_subscription(subscription_id: int, db: Session = Depends(get_db)):
    sub = subscription_service.get_subscription(db, subscription_id)
    return _enrich(sub)


@router.put("/{subscription_id}", response_model=SubscriptionResponse)
def update_subscription(subscription_id: int, data: SubscriptionUpdate, db: Session = Depends(get_db)):
    sub = subscription_service.update_subscription(db, subscription_id, data)
    return _enrich(sub)


@router.get("/{subscription_id}/invoice", dependencies=[])
def download_invoice(subscription_id: int, db: Session = Depends(get_db)):
    """Generate and download invoice PDF on-demand."""
    sub = subscription_service.get_subscription(db, subscription_id)
    
    # Verify subscription has payment data
    if not sub.amount or not sub.payment_date:
        raise HTTPException(status_code=400, detail="Subscription has no payment data")
    
    # Get member details
    if not sub.member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Generate PDF in memory
    pdf_buffer = generate_invoice_pdf(
        payment_id=sub.id,
        member_code=sub.member.member_id,
        member_name=sub.member.name,
        member_phone=sub.member.phone,
        amount=sub.amount,
        payment_date=sub.payment_date,
    )
    
    # Return PDF as streaming response
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=invoice_{sub.id}.pdf"
        }
    )
