import pytest
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models.user import User, UserCreate
from src.models.task import Task, TaskCreate
from src.models.task_tag import TaskTag, TaskTagCreate
from src.models.recurrence import RecurrencePattern, RecurrencePatternCreate


def test_user_model_creation():
    """Test User model creation"""
    user = User(
        email="test@example.com",
        hashed_password="hashed_password"
    )

    assert user.email == "test@example.com"
    assert user.hashed_password == "hashed_password"
    assert user.is_active is True  # Default value
    assert user.id is None  # Should be None before saving


def test_user_create_schema():
    """Test UserCreate schema"""
    user_create = UserCreate(
        email="test@example.com",
        password="password123"
    )

    assert user_create.email == "test@example.com"
    assert user_create.password == "password123"


def test_task_model_creation():
    """Test Task model creation"""
    task = Task(
        title="Test Task",
        description="Test Description",
        status="pending",
        priority="medium",
        user_id=1
    )

    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.status == "pending"
    assert task.priority == "medium"
    assert task.user_id == 1
    assert task.is_recurring is False  # Default value


def test_task_create_schema():
    """Test TaskCreate schema"""
    task_create = TaskCreate(
        title="Test Task",
        description="Test Description",
        status="pending",
        priority="medium",
        user_id=1
    )

    assert task_create.title == "Test Task"
    assert task_create.description == "Test Description"
    assert task_create.status == "pending"
    assert task_create.priority == "medium"
    assert task_create.user_id == 1


def test_task_model_defaults():
    """Test Task model default values"""
    task = Task(
        title="Test Task",
        priority="high",
        user_id=1
    )

    assert task.status == "pending"  # Default status
    assert task.is_recurring is False  # Default value
    assert task.title == "Test Task"


def test_task_tag_model_creation():
    """Test TaskTag model creation"""
    task_tag = TaskTag(
        task_id=1,
        tag_name="important"
    )

    assert task_tag.task_id == 1
    assert task_tag.tag_name == "important"


def test_task_tag_create_schema():
    """Test TaskTagCreate schema"""
    task_tag_create = TaskTagCreate(
        task_id=1,
        tag_name="important"
    )

    assert task_tag_create.task_id == 1
    assert task_tag_create.tag_name == "important"


def test_recurrence_pattern_model_creation():
    """Test RecurrencePattern model creation"""
    recurrence = RecurrencePattern(
        user_id=1,
        pattern_type="daily",
        interval=1,
        end_condition_type="never"
    )

    assert recurrence.user_id == 1
    assert recurrence.pattern_type == "daily"
    assert recurrence.interval == 1
    assert recurrence.end_condition_type == "never"
    assert recurrence.end_count is None  # Optional field
    assert recurrence.end_date is None  # Optional field


def test_recurrence_pattern_create_schema():
    """Test RecurrencePatternCreate schema"""
    recurrence_create = RecurrencePatternCreate(
        user_id=1,
        pattern_type="weekly",
        interval=2,
        end_condition_type="after_count",
        end_count=5
    )

    assert recurrence_create.user_id == 1
    assert recurrence_create.pattern_type == "weekly"
    assert recurrence_create.interval == 2
    assert recurrence_create.end_condition_type == "after_count"
    assert recurrence_create.end_count == 5


def test_recurrence_pattern_validation():
    """Test RecurrencePattern validation constraints"""
    # Test with minimum interval
    recurrence = RecurrencePattern(
        user_id=1,
        pattern_type="daily",
        interval=1,  # Minimum allowed
        end_condition_type="never"
    )

    assert recurrence.interval >= 1


def test_user_model_optional_fields():
    """Test User model with optional fields"""
    user = User(
        email="test@example.com",
        hashed_password="hashed_password",
        is_active=False
    )

    assert user.email == "test@example.com"
    assert user.hashed_password == "hashed_password"
    assert user.is_active is False  # Overridden default


def test_task_model_optional_fields():
    """Test Task model with optional fields"""
    now = datetime.utcnow()
    task = Task(
        title="Test Task",
        priority="high",
        user_id=1,
        due_date=now,
        description="A task with due date"
    )

    assert task.title == "Test Task"
    assert task.priority == "high"
    assert task.user_id == 1
    assert task.due_date == now
    assert task.description == "A task with due date"


if __name__ == "__main__":
    pytest.main()