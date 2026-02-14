from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional


class FeedbackCreate(BaseModel):
    """Schema for creating feedback (public API)"""
    name: str = Field(..., min_length=1, max_length=255, description="Customer name")
    email: EmailStr = Field(..., description="Customer email")
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    description: Optional[str] = Field(None, max_length=5000, description="Feedback description")
    
    @field_validator('rating')
    @classmethod
    def validate_rating(cls, v):
        if v < 1 or v > 5:
            raise ValueError('Rating must be between 1 and 5')
        return v


class FeedbackResponse(BaseModel):
    """Schema for feedback response"""
    id: int
    name: str
    email: str
    rating: int
    description: Optional[str]
    screenshot_url: Optional[str]
    client_ip: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class FeedbackListResponse(BaseModel):
    """Schema for paginated feedback list"""
    total: int
    feedbacks: list[FeedbackResponse]
