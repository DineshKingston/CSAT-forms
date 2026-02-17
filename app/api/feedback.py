from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Request,Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.feedback import FeedbackCreate, FeedbackResponse
from app.models.feedback import Feedback
from app.core.s3 import s3_manager
from typing import Optional
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/feedback", tags=["feedback"])


@router.post("/", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
async def submit_feedback(
    request: Request,
    name: str = Form(..., min_length=1, max_length=255),
    email: str = Form(...),
    rating: int = Form(..., ge=1, le=5),
    description: Optional[str] = Form(None, max_length=5000),
    screenshot: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """
    Submit feedback (Public API - No authentication required)
    
    Captures:
    - Name, Email, Rating (1-5), Description
    - Optional screenshot (uploaded to S3)
    - Client IP address
    - Timestamp (auto-generated)
    """
    # Validate rating
    if rating < 1 or rating > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 1 and 5"
        )
    
    # Extract client IP from forwarded headers (nginx proxy)
    # X-Forwarded-For contains the real client IP when behind a reverse proxy
    client_ip = (
        request.headers.get("X-Forwarded-For", "").split(",")[0].strip() or
        request.headers.get("X-Real-IP") or
        (request.client.host if request.client else None) or
        "unknown"
    )
    
    # Handle screenshot upload
    screenshot_url = None
    if screenshot:
        # Validate file type
        allowed_types = ["image/png", "image/jpeg", "image/jpg", "image/gif"]
        if screenshot.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only image files (PNG, JPEG, GIF) are allowed"
            )
        
        # Upload to S3
        file_content = await screenshot.read()
        file_extension = screenshot.filename.split(".")[-1] if "." in screenshot.filename else "png"
        screenshot_url = s3_manager.upload_file(file_content, file_extension)
        
        if screenshot_url is None:
            logger.warning("S3 upload failed, proceeding without screenshot")
    
    # Create feedback record
    feedback = Feedback(
        name=name,
        email=email,
        rating=rating,
        description=description,
        screenshot_url=screenshot_url,
        client_ip=client_ip
    )
    
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    
    logger.info(f"Feedback submitted: ID={feedback.id}, Email={email}, Rating={rating}")
    
    return feedback


@router.get("/{feedback_id}", response_model=FeedbackResponse)
def get_feedback(
    feedback_id: int,
    db: Session = Depends(get_db)
):
    """Get feedback by ID (for testing purposes)"""
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    
    return feedback
