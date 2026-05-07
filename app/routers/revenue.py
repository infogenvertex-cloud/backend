from datetime import datetime
import logging
import calendar

from fastapi import APIRouter, Depends
from sqlalchemy import func, extract
from sqlalchemy.orm import Session

from app.models.admin import Admin
from app.models.payment import Payment
from app.schemas.revenue import MonthlyRevenue, RevenueHistoryResponse
from app.utils.deps import get_db, get_current_admin

router = APIRouter(prefix="/revenue", tags=["Revenue"])
logger = logging.getLogger(__name__)


@router.get("/history", response_model=RevenueHistoryResponse)
def get_revenue_history(
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    """
    Get monthly revenue history grouped by year and month.
    Returns all months that have payments, ordered from most recent to oldest.
    """
    try:
        logger.info("Revenue history endpoint called")
        
        # Query to get monthly revenue grouped by year and month
        monthly_data = (
            db.query(
                extract('year', Payment.payment_date).label('year'),
                extract('month', Payment.payment_date).label('month'),
                func.sum(Payment.amount).label('total_revenue'),
                func.count(Payment.id).label('payment_count')
            )
            .group_by(
                extract('year', Payment.payment_date),
                extract('month', Payment.payment_date)
            )
            .order_by(
                extract('year', Payment.payment_date).desc(),
                extract('month', Payment.payment_date).desc()
            )
            .all()
        )
        
        logger.info(f"Found {len(monthly_data)} months with revenue data")
        
        # Convert to response format
        monthly_revenue_list = []
        for row in monthly_data:
            year = int(row.year)
            month = int(row.month)
            month_name = calendar.month_name[month]
            
            monthly_revenue_list.append(
                MonthlyRevenue(
                    year=year,
                    month=month,
                    month_name=month_name,
                    total_revenue=float(row.total_revenue),
                    payment_count=int(row.payment_count)
                )
            )
        
        # Calculate total all-time revenue
        total_all_time_result = db.query(func.sum(Payment.amount)).scalar()
        total_all_time = float(total_all_time_result) if total_all_time_result else 0.0
        
        logger.info(f"Total all-time revenue: {total_all_time}")
        
        return RevenueHistoryResponse(
            monthly_data=monthly_revenue_list,
            total_all_time=total_all_time
        )
    
    except Exception as e:
        logger.error(f"Error fetching revenue history: {str(e)}", exc_info=True)
        # Return empty data instead of crashing
        return RevenueHistoryResponse(
            monthly_data=[],
            total_all_time=0.0
        )
