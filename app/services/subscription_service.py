from __future__ import annotations

from datetime import date, datetime, timedelta

from dateutil.relativedelta import relativedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.models.subscription import Subscription
from app.models.member import Member
from app.schemas.subscription import SubscriptionCreate, SubscriptionUpdate
# from app.services.invoice_service import generate_invoice  # COMMENTED OUT - Invoice generation disabled

PLAN_DURATIONS = {
    "1_month": relativedelta(months=1),
    "3_month": relativedelta(months=3),
    "6_month": relativedelta(months=6),
    "12_month": relativedelta(months=12),
}


def create_subscription(db: Session, data: SubscriptionCreate) -> tuple[Subscription, Member]:
    """Create subscription with payment tracking."""
    try:
        if data.plan not in PLAN_DURATIONS:
            raise HTTPException(status_code=400, detail=f"Invalid plan. Choose from: {list(PLAN_DURATIONS.keys())}")

        # Verify member exists
        member = db.query(Member).filter(Member.id == data.member_id).first()
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")

        # Calculate end date
        end_date = data.start_date + PLAN_DURATIONS[data.plan]
        
        # Parse payment_date if it's a string, otherwise use provided datetime or current time
        if data.payment_date:
            if isinstance(data.payment_date, str):
                payment_date = datetime.fromisoformat(data.payment_date.replace('Z', '+00:00'))
            else:
                payment_date = data.payment_date
        else:
            payment_date = datetime.utcnow()
        
        # Create subscription with payment tracking
        subscription = Subscription(
            member_id=data.member_id,
            plan=data.plan,
            start_date=data.start_date,
            end_date=end_date,
            status="active",
            amount=data.amount,
            payment_date=payment_date,
        )
        db.add(subscription)
        db.commit()
        db.refresh(subscription)
        
        return subscription, member
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        import logging
        logging.error(f"Error creating subscription: {str(e)}")
        logging.error(f"Data: member_id={data.member_id}, plan={data.plan}, amount={data.amount}, payment_date={data.payment_date}")
        raise HTTPException(status_code=500, detail=f"Error creating subscription: {str(e)}")


def get_subscriptions(db: Session, skip: int = 0, limit: int = 20) -> list[Subscription]:
    return db.query(Subscription).order_by(Subscription.payment_date.desc()).offset(skip).limit(limit).all()


def get_subscriptions_grouped(db: Session, page: int = 1, limit: int = 20) -> dict:
    """
    Get subscriptions grouped by member with pagination.
    Returns a dictionary with grouped data and pagination info.
    """
    # Calculate offset
    skip = (page - 1) * limit
    
    # Get total unique members count
    total_members = db.query(func.count(func.distinct(Subscription.member_id))).scalar()
    
    # Get unique member IDs with pagination
    member_ids_query = (
        db.query(Subscription.member_id)
        .group_by(Subscription.member_id)
        .order_by(desc(func.max(Subscription.payment_date)))
        .offset(skip)
        .limit(limit)
    )
    member_ids = [row[0] for row in member_ids_query.all()]
    
    # Get all subscriptions for these members
    subscriptions = (
        db.query(Subscription)
        .filter(Subscription.member_id.in_(member_ids))
        .order_by(Subscription.member_id, Subscription.payment_date.desc())
        .all()
    )
    
    # Group subscriptions by member
    grouped_data = {}
    for sub in subscriptions:
        if sub.member_id not in grouped_data:
            grouped_data[sub.member_id] = {
                "member_id": sub.member_id,
                "member_code": sub.member.member_id if sub.member else None,
                "member_name": sub.member.name if sub.member else None,
                "member_phone": sub.member.phone if sub.member else None,
                "subscriptions": [],
                "total_subscriptions": 0,
                "active_subscriptions": 0,
                "total_amount": 0.0,
            }
        
        grouped_data[sub.member_id]["subscriptions"].append({
            "id": sub.id,
            "plan": sub.plan,
            "start_date": str(sub.start_date),
            "end_date": str(sub.end_date),
            "status": sub.status,
            "amount": float(sub.amount) if sub.amount else 0.0,
            "payment_date": sub.payment_date.isoformat() if sub.payment_date else None,
        })
        grouped_data[sub.member_id]["total_subscriptions"] += 1
        if sub.status == "active":
            grouped_data[sub.member_id]["active_subscriptions"] += 1
        if sub.amount:
            grouped_data[sub.member_id]["total_amount"] += float(sub.amount)
    
    # Convert to list and sort by latest payment date
    result_list = list(grouped_data.values())
    
    return {
        "data": result_list,
        "pagination": {
            "page": page,
            "limit": limit,
            "total_members": total_members,
            "total_pages": (total_members + limit - 1) // limit if total_members > 0 else 0,
        }
    }


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
