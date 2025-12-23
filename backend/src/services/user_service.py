
from sqlmodel import Session, select
from uuid import UUID
from typing import Optional
from ..models.user import User, UserCreate
from ..utils.security import get_password_hash
from datetime import datetime


def create_user(session: Session, user_create: UserCreate) -> User:
    """Create a new user with hashed password"""
    # Hash the password
    hashed_password = get_password_hash(user_create.password)

    # Create user object
    user = User(
        name=user_create.name,
        email=user_create.email, 
        hashed_password=hashed_password
    )

    # Add to database
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """Get a user by email"""
    statement = select(User).where(User.email == email)
    
    user = session.exec(statement).first()

    return user


def get_user_by_id(session: Session, user_id: UUID) -> Optional[User]:
    """Get a user by UUID"""
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    return user


def update_user(session: Session, user_id: UUID, **kwargs) -> Optional[User]:
    """Update a user's information"""
    user = get_user_by_id(session, user_id)
    if not user:
        return None

    # Update fields dynamically
    for field, value in kwargs.items():
        if hasattr(user, field):
            setattr(user, field, value)

    # Update timestamp
    user.updated_at = datetime.utcnow()

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def delete_user(session: Session, user_id: UUID) -> bool:
    """Delete a user by UUID"""
    user = get_user_by_id(session, user_id)
    if not user:
        return False

    session.delete(user)
    session.commit()
    return True
