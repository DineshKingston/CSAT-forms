from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app.schemas.admin import AdminCreate, AdminLogin, Token, AdminResponse
from app.models.admin import Admin
from app.core.security import verify_password, get_password_hash, create_access_token
from app.utils.dependencies import get_current_admin
from app.config import settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/register", response_model=AdminResponse, status_code=status.HTTP_201_CREATED)
def register_admin(
    admin_data: AdminCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new admin user
    
    SECURITY: This endpoint is ONLY for initial setup.
    After creating the first admin, protect this endpoint or disable it.
    Set ALLOW_ADMIN_REGISTRATION=false in production.
    """
    from app.config import settings
    
    # Security check: Only allow if no admins exist OR if explicitly enabled
    admin_count = db.query(Admin).count()
    allow_registration = getattr(settings, 'ALLOW_ADMIN_REGISTRATION', True)
    
    if admin_count > 0 and not allow_registration:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin registration is disabled. Contact existing admin."
        )
    
    # Check if username already exists
    existing_admin = db.query(Admin).filter(Admin.username == admin_data.username).first()
    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    existing_email = db.query(Admin).filter(Admin.email == admin_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create admin user
    admin = Admin(
        username=admin_data.username,
        email=admin_data.email,
        hashed_password=get_password_hash(admin_data.password),
        is_active=True
    )
    
    db.add(admin)
    db.commit()
    db.refresh(admin)
    
    logger.info(f"Admin registered: {admin.username} (Total admins: {admin_count + 1})")
    
    return admin


@router.post("/login", response_model=Token)
def login_admin(
    login_data: AdminLogin,
    db: Session = Depends(get_db)
):
    """
    Admin login - Returns JWT access token
    """
    # Find admin by username
    admin = db.query(Admin).filter(Admin.username == login_data.username).first()
    
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(login_data.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if admin is active
    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(admin.id)},
        expires_delta=access_token_expires
    )
    
    logger.info(f"Admin logged in: {admin.username}")
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=AdminResponse)
def get_current_admin_info(
    current_admin: Admin = Depends(get_current_admin)
):
    """
    Get current admin user information
    
    Requires valid JWT token in Authorization header.
    Returns the authenticated admin's profile.
    """
    return current_admin
