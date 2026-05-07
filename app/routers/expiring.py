from datetime import datetime, timedelta
import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.admin import Admin
from app.models.member import Member
from app.models.payment import Payment
from app.schemas.member import MemberResponse
from app.utils.deps import get_db, get_current_admin
from app.utils.pagination import PaginatedResponse

router = APIRouter(prefix="/expiring", tags=["Expiring"])

logger = logging.getLogger(__name__)


def calculate_expiry_date(payment_date: datetime, plan: str) -> datetime:
    """Calculate when a subscription expires based on plan"""
    plan_durations = {
        "1_month": 30,
        "3_month": 90,
        "6_month": 180,
        "12_month": 365,
    }
    
    days = plan_durations.get(plan, 30)  # Default to 30 days if plan not found
    return payment_date + timedelta(days=days)


class ExpiringMemberResponse(MemberResponse):
    """Extended member response with expiry information"""
    last_payment_date: Optional[datetime] = None
    last_plan: Optional[str] = None
    expiry_date: Optional[datetime] = None
    days_until_expiry: Optional[int] = None
    
    class Config:
        from_attributes = True


@router.get("/", response_model=PaginatedResponse[ExpiringMemberResponse])
def get_expiring_members(
    days: int = Query(7, description="Number of days to look ahead for expiring subscriptions"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    """
    Get members whose subscriptions are expiring soon with pagination.
    
    Logic:
    1. Find each member's latest payment
    2. Calculate expiry date based on payment date + plan duration
    3. Check if expiry date is within the specified days
    4. Return paginated members with expiry information
    """
    try:
        logger.info(f"Fetching members expiring within {days} days (page {page})")
        
        # Get all members
        members = db.query(Member).all()
        expiring_members = []
        
        today = datetime.utcnow()
        threshold_date = today + timedelta(days=days)
        
        for member in members:
            # Get member's latest payment
            latest_payment = (
                db.query(Payment)
                .filter(Payment.member_id == member.id)
                .order_by(Payment.payment_date.desc())
                .first()
            )
            
            if not latest_payment:
                # No payments, skip this member
                continue
            
            # Calculate expiry date
            expiry_date = calculate_expiry_date(latest_payment.payment_date, latest_payment.plan)
            
            # Check if expiring soon
            if today <= expiry_date <= threshold_date:
                days_until_expiry = (expiry_date - today).days
                
                # Create response with expiry info
                member_data = ExpiringMemberResponse(
                    id=member.id,
                    member_id=member.member_id,
                    name=member.name,
                    phone=member.phone,
                    join_date=member.join_date,
                    last_payment_date=latest_payment.payment_date,
                    last_plan=latest_payment.plan,
                    expiry_date=expiry_date,
                    days_until_expiry=days_until_expiry,
                )
                
                expiring_members.append(member_data)
        
        # Sort by days until expiry (most urgent first)
        expiring_members.sort(key=lambda x: x.days_until_expiry if x.days_until_expiry is not None else 999)
        
        # Paginate
        total = len(expiring_members)
        skip = (page - 1) * page_size
        paginated_items = expiring_members[skip:skip + page_size]
        
        logger.info(f"Found {total} members expiring soon, returning page {page}")
        
        return PaginatedResponse.create(
            items=paginated_items,
            total=total,
            page=page,
            page_size=page_size
        )
    
    except Exception as e:
        logger.error(f"Error fetching expiring members: {str(e)}", exc_info=True)
        # Return empty paginated response instead of crashing
        return PaginatedResponse.create(
            items=[],
            total=0,
            page=page,
            page_size=page_size
        )


@router.get("/count")
def get_expiring_count(
    days: int = Query(7, description="Number of days to look ahead"),
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    """Get count of members expiring soon (for dashboard widget)"""
    try:
        members = db.query(Member).all()
        count = 0
        
        today = datetime.utcnow()
        threshold_date = today + timedelta(days=days)
        
        for member in members:
            latest_payment = (
                db.query(Payment)
                .filter(Payment.member_id == member.id)
                .order_by(Payment.payment_date.desc())
                .first()
            )
            
            if latest_payment:
                expiry_date = calculate_expiry_date(latest_payment.payment_date, latest_payment.plan)
                if today <= expiry_date <= threshold_date:
                    count += 1
        
        return {"count": count, "days": days}
    
    except Exception as e:
        logger.error(f"Error counting expiring members: {str(e)}")
        return {"count": 0, "days": days}
