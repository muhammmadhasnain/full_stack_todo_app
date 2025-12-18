"""
Test database setup for end-to-end tests
"""
from sqlmodel import SQLModel, create_engine
from sqlmodel.pool import StaticPool
from backend.src.models.user import User
from backend.src.models.task import Task
from backend.src.models.task_tag import TaskTag
from backend.src.models.recurrence import RecurrencePattern


def create_test_engine():
    """Create an in-memory database engine for testing"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    return engine


def create_test_database():
    """Create the test database with all tables"""
    engine = create_test_engine()
    SQLModel.metadata.create_all(bind=engine)
    return engine