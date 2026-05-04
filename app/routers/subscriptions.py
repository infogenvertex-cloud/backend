from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.subscription import SubscriptionCreate, SubscriptionUpdate, SubscriptionResponse
from app.services import subscription_service
from app.utils.deps import get_db, get_current_admin

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"], dependencies=[Depends(get_current_admin)])


def _enrich(sub):
    """Add member details from the related member."""
    # Use from_attributes to properly handle SQLAlchemy models with NULL values
    resp = SubscriptionResponse.model_validate(sub, from_attributes=True)
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
