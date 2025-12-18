import pytest
from unittest.mock import Mock, patch, MagicMock
from sqlmodel import Session, select
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models.user import User
from src.schemas.user import UserCreate, UserLogin
from src.services.auth_service import register_user, login_user
from src.services.user_service import get_user_by_email


@pytest.fixture
def mock_session():
    """Mock database session for testing"""
    session = Mock(spec=Session)
    return session


@pytest.fixture
def sample_user_create():
    """Sample user creation data"""
    return UserCreate(
        email="test@example.com",
        password="password123"
    )


@pytest.fixture
def sample_user_login():
    """Sample user login data"""
    return UserLogin(
        email="test@example.com",
        password="password123"
    )


def test_register_user_success(mock_session, sample_user_create):
    """Test successful user registration"""
    with patch('src.services.user_service.create_user') as mock_create_user:
        # Mock user creation
        mock_user = User(
            id=1,
            email=sample_user_create.email,
            hashed_password="hashed_password",
        )
        mock_create_user.return_value = mock_user

        result = register_user(mock_session, sample_user_create)

        assert result == mock_user
        mock_create_user.assert_called_once()


def test_login_user_success(mock_session, sample_user_login):
    """Test successful user login"""
    with patch('src.services.auth_service.authenticate_user') as mock_auth_user:
        # Mock authenticated user
        mock_user = User(
            id=1,
            email=sample_user_login.email,
            hashed_password="hashed_password",
            created_at=None,
            updated_at=None
        )
        mock_auth_user.return_value = mock_user

        with patch('src.services.auth_service.create_access_token') as mock_create_access:
            with patch('src.services.auth_service.create_refresh_token') as mock_create_refresh:
                mock_create_access.return_value = "mock_access_token"
                mock_create_refresh.return_value = "mock_refresh_token"

                result = login_user(mock_session, sample_user_login)

                assert result is not None
                assert result["access_token"] == "mock_access_token"
                assert result["refresh_token"] == "mock_refresh_token"
                assert result["user_id"] == 1


def test_login_user_invalid_credentials(mock_session, sample_user_login):
    """Test login with invalid credentials"""
    with patch('src.services.auth_service.authenticate_user') as mock_auth_user:
        mock_auth_user.return_value = None

        result = login_user(mock_session, sample_user_login)

        assert result is None


def test_login_user_not_found(mock_session, sample_user_login):
    """Test login when user doesn't exist"""
    with patch('src.services.auth_service.authenticate_user') as mock_auth_user:
        mock_auth_user.return_value = None

        result = login_user(mock_session, sample_user_login)

        assert result is None


if __name__ == "__main__":
    pytest.main()