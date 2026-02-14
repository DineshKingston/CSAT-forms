from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class AdminCreate(BaseModel):
    """Schema for creating admin user"""
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)


class AdminLogin(BaseModel):
    """Schema for admin login"""
    username: str
    password: str


class AdminResponse(BaseModel):
    """Schema for admin response (without password)"""
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Schema for JWT token payload"""
    sub: Optional[int] = None  # subject (user id)
    exp: Optional[int] = None  # expiration time
