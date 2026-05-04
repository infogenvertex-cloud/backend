from __future__ import annotations

from datetime import date, timedelta

from dateutil.relativedelta import relativedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.subscription import Subscription
from app.models.member import Member
from app.schemas.subscription import SubscriptionCreate, SubscriptionUpdate
from app.services.invoice_service import generate_invoice

PLAN_DURATIONS = {
    "1_month": relativedelta(months=1),
    "3_month": relativedelta(months=3),
    "6_month": relativedelta(months=6),
    "12_month": relativedelta(months=12),
}


def create_subscription(db: Session, data: SubscriptionCreate) -> tuple[Subscription, Member]:
    """Create subscription with payment in a single transaction."""
    if data.plan not in PLAN_DURATIONS:
        raise HTTPException(status_code=400, detail=f"Invalid plan. Choose from: {list(PLAN_DURATIONS.keys())}")

    # Verify member exists
    member = db.query(Member).filter(Member.id == data.member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    # Calculate end date
    end_date = data.start_date + PLAN_DURATIONS[data.plan]
    
    # Create subscription with payment
    from datetime import datetime
    subscription = Subscription(
        member_id=data.member_id,
        plan=data.plan,
        start_date=data.start_date,
        end_date=end_date,
        status="active",
        amount=data.amount,
        payment_date=datetime.utcnow(),  # Explicitly set payment_date
    )
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    
    # Generate invoice
    invoice_url = generate_invoice(
        payment_id=subscription.id,
        member_code=member.member_id,
        member_name=member.name,
        member_phone=member.phone,
        amount=subscription.amount,
        payment_date=subscription.payment_date,
    )
    subscription.invoice_url = invoice_url
    db.commit()
    db.refresh(subscription)
    
    return subscription, member


def get_subscriptions(db: Session, skip: int = 0, limit: int = 100) -> list[Subscription]:
    return db.query(Subscription).order_by(Subscription.payment_date.desc()).offset(skip).limit(limit).all()


def get_subscription(db: Session, subscription_id: int) -> Subscription:
    sub = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return sub


def get_member_subscriptions(db: Session, member_id: int) -> list[Subscription]:
    return db.query(Subscription).filter(Subscription.member_id == member_id).order_by(Subscription.payment_date.desc()).all()


def update_subscription(db: Session, subscription_id: int, data: SubscriptionUpdate) -> Subscription:
    sub = get_subscription(db, subscription_id)
    update_data = data.model_dump(exclude_unset=True)

    if "plan" in update_data or "start_date" in update_data:
        plan = update_data.get("plan", sub.plan)
        start = update_data.get("start_date", sub.start_date)
        if plan not in PLAN_DURATIONS:
            raise HTTPException(status_code=400, detail=f"Invalid plan. Choose from: {list(PLAN_DURATIONS.keys())}")
        sub.plan = plan
        sub.start_date = start
        sub.end_date = start + PLAN_DURATIONS[plan]

    if "status" in update_data:
        sub.status = update_data["status"]

    db.commit()
    db.refresh(sub)
    return sub


def get_expiring_subscriptions(db: Session, days: int = 5) -> list[Subscription]:
    today = date.today()
    deadline = today + timedelta(days=days)
    return (
        db.query(Subscription)
        .filter(
            Subscription.status == "active",
            Subscription.end_date >= today,
            Subscription.end_date <= deadline,
        )
        .all()
    )


def expire_overdue_subscriptions(db: Session) -> int:
    today = date.today()
    count = (
        db.query(Subscription)
        .filter(Subscription.status == "active", Subscription.end_date < today)
        .update({"status": "expired"})
    )
    db.commit()
    return count
