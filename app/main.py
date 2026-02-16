from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api import feedback_router, admin_router, analytics_router
from app.config import settings
from app.database import engine, Base
from app.models import *  # Import all models
from sqlalchemy import text

# Create database table
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Customer Satisfaction (CSAT) Feedback Collection and Analytics System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(feedback_router)
app.include_router(admin_router)
app.include_router(analytics_router)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Welcome to ClientPulse API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint with database verification
    Returns 200 if healthy, 503 if unhealthy
    """
    health_status = {
        "status": "healthy",
        "database": "unknown",
        "s3": "disabled"
    }
    
    # Check database connection
    try:
        # Use engine directly instead of get_db() to avoid generator issues
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        health_status["database"] = "connected"
    except Exception as e:
        logger.error(f"Health check failed - Database error: {str(e)}")
        health_status["status"] = "unhealthy"
        health_status["database"] = "disconnected"
        raise HTTPException(
            status_code=503,
            detail="Service unavailable - Database connection failed"
        )
    
    # Check S3 status
    try:
        from app.core.s3 import s3_manager
        if s3_manager.enabled:
            health_status["s3"] = "enabled"
    except Exception:
        # S3 check is optional, don't fail health check if it errors
        health_status["s3"] = "not configured"
    
    return health_status


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
