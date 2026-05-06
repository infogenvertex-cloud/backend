from datetime import date, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.admin import Admin
from app.models.member import Member
from app.models.subscription import Subscription
from app.schemas.dashboard import DashboardStats
from app.schemas.subscription import SubscriptionResponse
from app.utils.deps import get_db, get_current_admin

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/", response_model=DashboardStats)
def get_dashboard(
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    total_members = db.query(Member).count()

    active_members = (
        db.query(Subscription.member_id)
        .filter(Subscription.status == "active")
        .distinct()
        .count()
    )

    today = date.today()
    expiring_soon = (
        db.query(Subscription)
        .filter(
            Subscription.status == "active",
            Subscription.end_date >= today,
            Subscription.end_date <= today + timedelta(days=5),
        )
        .count()
    )

    # Get recent subscriptions with payments (amount is not null)
    recent_payments = (
        db.query(Subscription)
        .filter(Subscription.amount.isnot(None))  # Only subscriptions with payment
        .order_by(Subscription.start_date.desc())  # Order by start date
        .limit(10)
        .all()
    )

    enriched_payments = []
    for sub in recent_payments:
        resp = SubscriptionResponse.model_validate(sub, from_attributes=True)
        if sub.member:
            resp.member_code = sub.member.member_id
            resp.member_name = sub.member.name
            resp.member_phone = sub.member.phone
        enriched_payments.append(resp)

    return DashboardStats(
        total_members=total_members,
        active_members=active_members,
        expiring_soon=expiring_soon,
        recent_payments=enriched_payments,
    )
