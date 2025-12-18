from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from ..database.session import get_session
from ..schemas.user import UserRegister, UserLogin, UserProfile
from ..schemas.auth import AuthResponse, RefreshTokenRequest, RefreshTokenResponse
from ..services.auth_service import register_user, login_user, refresh_access_token
from ..services.user_service import get_user_by_id
from .deps import get_current_user

router = APIRouter()


@router.post("/register", response_model=AuthResponse)
def register(user_register: UserRegister, session: Session = Depends(get_session)):
    """Register a new user"""
    from ..services.user_service import get_user_by_email

    # Check if user already exists
    existing_user = get_user_by_email(session, user_register.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # Register the user
    user = register_user(session, user_register)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not register user"
        )

    # Create response with tokens
    auth_result = login_user(session, UserLogin(email=user_register.email, password=user_register.password))
    if not auth_result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not generate tokens after registration"
        )

    # Create user profile
    user_profile = UserProfile(
        id=auth_result["user_id"],
        name=user.name,
        email=auth_result["email"],
        created_at=user.created_at,
        updated_at=user.updated_at,
        is_active=user.is_active
    )

    return AuthResponse(
        access_token=auth_result["access_token"],
        token_type=auth_result["token_type"],
        refresh_token=auth_result["refresh_token"],
        user=user_profile
    )


@router.post("/login", response_model=AuthResponse)
def login(user_login: UserLogin, session: Session = Depends(get_session)):
    """Authenticate user and return tokens"""
    auth_result = login_user(session, user_login)
    if not auth_result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user details
    user = get_user_by_id(session, auth_result["user_id"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Create user profile
    user_profile = UserProfile(
        id=auth_result["user_id"],
        name=user.name,
        email=auth_result["email"],
        created_at=user.created_at,
        updated_at=user.updated_at,
        is_active=user.is_active
    )

    return AuthResponse(
        access_token=auth_result["access_token"],
        token_type=auth_result["token_type"],
        refresh_token=auth_result["refresh_token"],
        user=user_profile
    )


@router.post("/refresh", response_model=RefreshTokenResponse)
def refresh_token(refresh_request: RefreshTokenRequest):
    """Refresh access token using refresh token"""
    result = refresh_access_token(refresh_request.refresh_token)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return RefreshTokenResponse(
        access_token=result["access_token"],
        token_type=result["token_type"]
    )


@router.get("/me", response_model=UserProfile)
def get_profile(current_user: dict = Depends(get_current_user), session: Session = Depends(get_session)):
    """Get current user profile"""
    user = get_user_by_id(session, current_user["user_id"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserProfile(
        id=user.id,
        name=user.name,
        email=user.email,
        created_at=user.created_at,
        updated_at=user.updated_at,
        is_active=user.is_active
    )