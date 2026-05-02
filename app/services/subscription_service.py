from __future__ import annotations

from datetime import date, timedelta

from dateutil.relativedelta import relativedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.subscription import Subscription
from app.schemas.subscription import SubscriptionCreate, SubscriptionUpdate

PLAN_DURATIONS = {
    "1_month": relativedelta(months=1),
    "3_month": relativedelta(months=3),
    "6_month": relativedelta(months=6),
    "12_month": relativedelta(months=12),
}


def create_subscription(db: Session, data: SubscriptionCreate) -> Subscription:
    if data.plan not in PLAN_DURATIONS:
        raise HTTPException(status_code=400, detail=f"Invalid plan. Choose from: {list(PLAN_DURATIONS.keys())}")

    end_date = data.start_date + PLAN_DURATIONS[data.plan]
    subscription = Subscription(
        member_id=data.member_id,
        plan=data.plan,
        start_date=data.start_date,
        end_date=end_date,
        status="active",
    )
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription


def get_subscriptions(db: Session, skip: int = 0, limit: int = 100) -> list[Subscription]:
    return db.query(Subscription).offset(skip).limit(limit).all()


def get_subscription(db: Session, subscription_id: int) -> Subscription:
    sub = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return sub


def get_member_subscriptions(db: Session, member_id: int) -> list[Subscription]:
    return db.query(Subscription).filter(Subscription.member_id == member_id).all()


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
