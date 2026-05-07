from pydantic import BaseModel


class MonthlyRevenue(BaseModel):
    """Monthly revenue data"""
    year: int
    month: int
    month_name: str
    total_revenue: float
    payment_count: int


class RevenueHistoryResponse(BaseModel):
    """Response containing revenue history"""
    monthly_data: list[MonthlyRevenue]
    total_all_time: float
