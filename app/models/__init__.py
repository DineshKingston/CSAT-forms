"""Models package - Import all models here for Alembic discovery"""
from app.models.feedback import Feedback
from app.models.admin import Admin

__all__ = ["Feedback", "Admin"]
