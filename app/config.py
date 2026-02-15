from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "ClientPulse"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Security
    ALLOW_ADMIN_REGISTRATION: bool = True  # Set to False in production after first admin
    
    # Database
    DATABASE_URL: str
    
    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # AWS S3
    AWS_ACCESS_KEY_ID: str = ""  # Optional - gracefully handle if not set
    AWS_SECRET_ACCESS_KEY: str = ""  # Optional
    AWS_REGION: str = "us-east-1"
    AWS_S3_BUCKET_NAME: str = ""  # Optional
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
