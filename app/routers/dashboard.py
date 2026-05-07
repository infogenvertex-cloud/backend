from datetime import datetime, timedelta
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.admin import Admin
from app.models.member import Member
from app.models.payment import Payment
from app.models.visitor import Visitor
from app.schemas.dashboard import DashboardStats
from app.schemas.payment import PaymentResponse
from app.utils.deps import get_db, get_current_admin

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

logger = logging.getLogger(__name__)


def calculate_expiry_date(payment_date: datetime, plan: str) -> datetime:
    """Calculate when a subscription expires based on plan"""
    plan_durations = {
        "1_month": 30,
        "3_month": 90,
        "6_month": 180,
        "12_month": 365,
    }
    
    days = plan_durations.get(plan, 30)
    return payment_date + timedelta(days=days)


def is_member_active(db: Session, member_id: int) -> bool:
    """Check if a member has an active subscription"""
    try:
        # Get member's latest payment
        latest_payment = (
            db.query(Payment)
            .filter(Payment.member_id == member_id)
            .order_by(Payment.payment_date.desc())
            .first()
        )
        
        if not latest_payment:
            return False
        
        # Calculate expiry date
        expiry_date = calculate_expiry_date(latest_payment.payment_date, latest_payment.plan)
        
        # Check if still active (expiry date is in the future)
        return expiry_date >= datetime.utcnow()
    except Exception as e:
        logger.error(f"Error checking member active status: {e}")
        return False


@router.get("/", response_model=DashboardStats)
def get_dashboard(
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    try:
        logger.info("Dashboard endpoint called")
        
        # Total members
        try:
            total_members = db.query(Member).count()
            logger.info(f"Total members: {total_members}")
        except Exception as e:
            logger.error(f"Error counting members: {e}")
            total_members = 0
        
        # Active members (members with active subscriptions)
        try:
            all_members = db.query(Member).all()
            active_members = sum(1 for member in all_members if is_member_active(db, member.id))
            logger.info(f"Active members: {active_members}")
        except Exception as e:
            logger.error(f"Error counting active members: {e}")
            active_members = 0
        
        # Total visitors
        try:
            total_visitors = db.query(Visitor).count()
            logger.info(f"Total visitors: {total_visitors}")
        except Exception as e:
            logger.error(f"Error counting visitors: {e}")
            total_visitors = 0
        
        # Total payment amount
        try:
            total_payments_result = db.query(func.sum(Payment.amount)).scalar()
            total_payments = float(total_payments_result) if total_payments_result else 0.0
            logger.info(f"Total payments: {total_payments}")
        except Exception as e:
            logger.error(f"Error calculating total payments: {e}")
            total_payments = 0.0
        
        # Monthly revenue (current month)
        try:
            # Get first day of current month
            today = datetime.utcnow()
            first_day_of_month = datetime(today.year, today.month, 1)
            
            # Calculate sum of payments in current month
            monthly_revenue_result = (
                db.query(func.sum(Payment.amount))
                .filter(Payment.payment_date >= first_day_of_month)
                .scalar()
            )
            monthly_revenue = float(monthly_revenue_result) if monthly_revenue_result else 0.0
            logger.info(f"Monthly revenue: {monthly_revenue}")
        except Exception as e:
            logger.error(f"Error calculating monthly revenue: {e}")
            monthly_revenue = 0.0
        
        # Recent visitors count (last 7 days)
        try:
            seven_days_ago = datetime.utcnow() - timedelta(days=7)
            recent_visitors_count = db.query(Visitor).filter(Visitor.visited_at >= seven_days_ago).count()
            logger.info(f"Recent visitors: {recent_visitors_count}")
        except Exception as e:
            logger.error(f"Error counting recent visitors: {e}")
            recent_visitors_count = 0
        
        # Get recent payments (last 10)
        try:
            recent_payments = (
                db.query(Payment)
                .order_by(Payment.payment_date.desc())
                .limit(10)
                .all()
            )
            logger.info(f"Found {len(recent_payments)} recent payments")
        except Exception as e:
            logger.error(f"Error fetching recent payments: {e}")
            recent_payments = []
        
        # Enrich payment responses with member details
        enriched_payments = []
        for payment in recent_payments:
            try:
                resp = PaymentResponse.model_validate(payment, from_attributes=True)
                if payment.member:
                    resp.member_code = payment.member.member_id
                    resp.member_name = payment.member.name
                    resp.member_phone = payment.member.phone
                enriched_payments.append(resp)
            except Exception as e:
                logger.error(f"Error enriching payment {payment.id}: {e}")
                # Still add the payment without member details
                try:
                    resp = PaymentResponse.model_validate(payment, from_attributes=True)
                    enriched_payments.append(resp)
                except Exception as e2:
                    logger.error(f"Error creating payment response for {payment.id}: {e2}")
                    continue
        
        logger.info("Dashboard data prepared successfully")
        
        return DashboardStats(
            total_members=total_members,
            active_members=active_members,
            total_visitors=total_visitors,
            total_payments=total_payments,
            monthly_revenue=monthly_revenue,
            recent_payments=enriched_payments,
            recent_visitors_count=recent_visitors_count,
        )
    
    except Exception as e:
        logger.error(f"Dashboard endpoint error: {str(e)}", exc_info=True)
        # Return empty dashboard instead of crashing
        return DashboardStats(
            total_members=0,
            active_members=0,
            total_visitors=0,
            total_payments=0.0,
            monthly_revenue=0.0,
            recent_payments=[],
            recent_visitors_count=0,
        )
