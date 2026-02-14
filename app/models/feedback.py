from sqlalchemy import Column, Integer, String, Text, DateTime, CheckConstraint
from sqlalchemy.sql import func
from app.database import Base


class Feedback(Base):
    """Feedback model for storing customer satisfaction surveys"""
    
    __tablename__ = "feedbacks"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    rating = Column(Integer, CheckConstraint('rating >= 1 AND rating <= 5'), nullable=False)
    description = Column(Text, nullable=True)
    screenshot_url = Column(String(500), nullable=True)
    client_ip = Column(String(45), nullable=True)  # IPv6 max length
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Feedback(id={self.id}, email={self.email}, rating={self.rating})>"
