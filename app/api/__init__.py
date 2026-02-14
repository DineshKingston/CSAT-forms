"""API package - Import all routers"""
from app.api.feedback import router as feedback_router
from app.api.admin import router as admin_router
from app.api.analytics import router as analytics_router

__all__ = ["feedback_router", "admin_router", "analytics_router"]
