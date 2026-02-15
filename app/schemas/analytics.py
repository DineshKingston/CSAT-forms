from pydantic import BaseModel
from typing import Dict


class AnalyticsReport(BaseModel):
    """Schema for analytics report"""
    total_feedbacks: int
    overall_avg_rating: float
    avg_rating_last_30_days: float
    avg_rating_last_60_days: float
    avg_rating_last_90_days: float
    rating_distribution: Dict[str, int]  # {"1": 10, "2": 20, ...}


class DownloadFormat(BaseModel):
    """Schema for download format query param"""
    format: str = "csv"  # csv or json
