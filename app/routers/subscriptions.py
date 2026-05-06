from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.admin import Admin
from app.schemas.subscription import SubscriptionCreate, SubscriptionUpdate, SubscriptionResponse
from app.services import subscription_service
from app.utils.deps import get_db, get_current_admin

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


def _enrich(sub):
    resp = SubscriptionResponse(
        id=sub.id,
        member_id=sub.member_id,
        plan=sub.plan,
        start_date=sub.start_date,
        end_date=sub.end_date,
        status=sub.status,
        amount=sub.amount,
        payment_date=sub.payment_date,
    )
    if sub.member:
        resp.member_code = sub.member.member_id
        resp.member_name = sub.member.name
        resp.member_phone = sub.member.phone
    return resp


@router.post("/", response_model=SubscriptionResponse, status_code=201)
def create_subscription(
    data: SubscriptionCreate,
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    subscription, member = subscription_service.create_subscription(db, data)
    return _enrich(subscription)


@router.get("/", response_model=List[SubscriptionResponse])
def list_subscriptions(
    member_id: int = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    if member_id is not None:
        subs = subscription_service.get_member_subscriptions(db, member_id)
    else:
        subs = subscription_service.get_subscriptions(db, skip, limit)
    return [_enrich(s) for s in subs]


@router.get("/grouped")
def list_subscriptions_grouped(
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    return subscription_service.get_subscriptions_grouped(db, page, limit)


@router.get("/{subscription_id:int}", response_model=SubscriptionResponse)
def get_subscription(
    subscription_id: int,
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    sub = subscription_service.get_subscription(db, subscription_id)
    return _enrich(sub)


@router.put("/{subscription_id:int}", response_model=SubscriptionResponse)
def update_subscription(
    subscription_id: int,
    data: SubscriptionUpdate,
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    sub = subscription_service.update_subscription(db, subscription_id, data)
    return _enrich(sub)
