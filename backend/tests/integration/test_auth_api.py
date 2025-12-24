import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.pool import StaticPool
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.main import app
from src.database.database import engine
from src.database.session import get_session
from src.models.user import User


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def test_register_user_success(client: TestClient):
    """Test successful user registration"""
    user_data = {
        "email": "test@example.com",
        "password": "password123"
    }

    response = client.post("/api/auth/register", json=user_data)

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert "user" in data
    assert data["user"]["email"] == "test@example.com"


def test_register_user_duplicate(client: TestClient):
    """Test registering a user that already exists"""
    user_data = {
        "email": "duplicate@example.com",
        "password": "password123"
    }

    # Register user first time
    response1 = client.post("/api/auth/register", json=user_data)
    assert response1.status_code == 200

    # Try to register same user again
    response2 = client.post("/api/auth/register", json=user_data)
    assert response2.status_code == 400


def test_login_user_success(client: TestClient):
    """Test successful user login"""
    # First register a user
    register_data = {
        "email": "login@example.com",
        "password": "password123"
    }
    register_response = client.post("/api/auth/register", json=register_data)
    assert register_response.status_code == 200

    # Then try to login
    login_data = {
        "email": "login@example.com",
        "password": "password123"
    }
    response = client.post("/api/auth/login", json=login_data)

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert "user" in data
    assert data["user"]["email"] == "login@example.com"


def test_login_user_invalid_credentials(client: TestClient):
    """Test login with invalid credentials"""
    # First register a user
    register_data = {
        "email": "invalid@example.com",
        "password": "password123"
    }
    register_response = client.post("/api/auth/register", json=register_data)
    assert register_response.status_code == 200

    # Try to login with wrong password
    login_data = {
        "email": "invalid@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/api/auth/login", json=login_data)

    assert response.status_code == 401


def test_get_user_profile_success(client: TestClient):
    """Test getting user profile with valid token"""
    # Register a user
    register_data = {
        "email": "profile@example.com",
        "password": "password123"
    }
    register_response = client.post("/api/auth/register", json=register_data)
    assert register_response.status_code == 200

    data = register_response.json()
    access_token = data["access_token"]

    # Get user profile with valid token
    response = client.get("/api/auth/me",
                         headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    profile_data = response.json()

    assert profile_data["email"] == "profile@example.com"


def test_get_user_profile_unauthorized(client: TestClient):
    """Test getting user profile without token"""
    response = client.get("/api/auth/me")

    assert response.status_code == 401


def test_refresh_token_success(client: TestClient):
    """Test refreshing access token with valid refresh token"""
    # Register a user
    register_data = {
        "email": "refresh@example.com",
        "password": "password123"
    }
    register_response = client.post("/api/auth/register", json=register_data)
    assert register_response.status_code == 200

    data = register_response.json()
    refresh_token = data["refresh_token"]

    # Refresh token
    refresh_data = {
        "refresh_token": refresh_token
    }
    response = client.post("/api/auth/refresh", json=refresh_data)

    assert response.status_code == 200
    refresh_data = response.json()

    assert "access_token" in refresh_data
    assert "token_type" in refresh_data


if __name__ == "__main__":
    pytest.main()