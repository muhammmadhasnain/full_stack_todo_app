

from sqlmodel import Session
from typing import Optional
from ..models.user import User
from ..schemas.user import UserCreate, UserLogin
from ..utils.security import (
    authenticate_user,
    create_access_token,
    create_refresh_token
)
from datetime import timedelta


def register_user(session: Session, user_create: UserCreate) -> Optional[User]:
    """Register a new user (UUID ready)"""
    from ..services.user_service import create_user
    return create_user(session, user_create)


def login_user(session: Session, user_login: UserLogin) -> Optional[dict]:
    """Authenticate user and return tokens (UUID ready)"""
    user = authenticate_user(
        session=session,
        email=user_login.email,
        password=user_login.password
    )

    if not user:
        return None

    # Get the user ID as string (since it's already a UUID)
    user_id = str(user.id)

    # Create access token
    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={"user_id": user_id, "email": user.email},
        expires_delta=access_token_expires
    )

    # Create refresh token
    refresh_token = create_refresh_token(
        data={"user_id": user_id, "email": user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
        "user_id": user_id,
        "email": user.email
    }


def refresh_access_token(refresh_token: str) -> Optional[dict]:
    """Refresh access token using refresh token (UUID ready)"""
    from ..utils.security import verify_token

    try:
        payload = verify_token(refresh_token)

        # Check if this is a refresh token
        if payload.get("type") != "refresh":
            return None

        user_id = str(payload.get("user_id"))  # ensure string UUID
        email = payload.get("email")

        if user_id is None or email is None:
            return None

        # Create new access token
        access_token_expires = timedelta(minutes=15)
        access_token = create_access_token(
            data={"user_id": user_id, "email": email},
            expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except Exception:
        return None
