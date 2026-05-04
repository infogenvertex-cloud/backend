from datetime import date, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.member import Member
from app.models.subscription import Subscription
from app.models.payment import Payment
from app.schemas.dashboard import DashboardStats
from app.schemas.payment import PaymentResponse
from app.utils.deps import get_db, get_current_admin

router = APIRouter(prefix="/dashboard", tags=["Dashboard"], dependencies=[Depends(get_current_admin)])


@router.get("/", response_model=DashboardStats)
def get_dashboard(db: Session = Depends(get_db)):
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

    recent_payments = (
        db.query(Payment)
        .order_by(Payment.payment_date.desc())
        .limit(10)
        .all()
    )

    enriched_payments = []
    for p in recent_payments:
        resp = PaymentResponse.model_validate(p)
        if p.member:
            resp.member_code = p.member.member_id
            resp.member_name = p.member.name
            resp.member_phone = p.member.phone
        enriched_payments.append(resp)

    return DashboardStats(
        total_members=total_members,
        active_members=active_members,
        expiring_soon=expiring_soon,
        recent_payments=enriched_payments,
    )
