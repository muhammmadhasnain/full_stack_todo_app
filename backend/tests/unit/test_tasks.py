import pytest
from unittest.mock import Mock, patch
from sqlmodel import Session
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models.task import Task
from src.schemas.task import TaskCreate, TaskUpdate
from src.services.task_service import (
    create_task, get_task_by_id, get_tasks_by_user, update_task, delete_task,
    toggle_task_completion
)


@pytest.fixture
def mock_session():
    """Mock database session for testing"""
    session = Mock(spec=Session)
    return session


@pytest.fixture
def sample_task_create():
    """Sample task creation data"""
    return TaskCreate(
        title="Test Task",
        description="Test Description",
        status="pending",
        priority="medium",
        user_id=1
    )


@pytest.fixture
def sample_task():
    """Sample task object"""
    return Task(
        id=1,
        title="Test Task",
        description="Test Description",
        status="pending",
        priority="medium",
        user_id=1,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )


def test_create_task_success(mock_session, sample_task_create):
    """Test successful task creation"""
    # Mock user exists
    mock_user = Mock()
    mock_session.get.return_value = mock_user

    # Mock task creation
    mock_task = Task(
        id=1,
        title=sample_task_create.title,
        description=sample_task_create.description,
        status=sample_task_create.status,
        priority=sample_task_create.priority,
        user_id=sample_task_create.user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    with patch('src.services.task_service.Task') as mock_task_class:
        mock_task_class.return_value = mock_task
        mock_session.add = Mock()
        mock_session.commit = Mock()
        mock_session.refresh = Mock()
        mock_session.refresh.return_value = mock_task

        result = create_task(mock_session, sample_task_create)

        assert result.id == 1
        assert result.title == "Test Task"
        assert result.user_id == 1
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()


def test_create_task_user_not_found(mock_session, sample_task_create):
    """Test task creation when user doesn't exist"""
    mock_session.get.return_value = None

    with pytest.raises(ValueError, match="User not found"):
        create_task(mock_session, sample_task_create)


def test_get_task_by_id_success(mock_session, sample_task):
    """Test successful task retrieval by ID"""
    with patch('src.services.task_service.select') as mock_select:
        with patch('src.services.task_service.and_') as mock_and:
            mock_exec = Mock()
            mock_exec.first.return_value = sample_task
            mock_session.exec.return_value = mock_exec

            result = get_task_by_id(mock_session, 1, 1)

            assert result == sample_task
            mock_session.exec.assert_called_once()


def test_get_task_by_id_not_found(mock_session):
    """Test task retrieval when task doesn't exist"""
    with patch('src.services.task_service.select') as mock_select:
        with patch('src.services.task_service.and_') as mock_and:
            mock_exec = Mock()
            mock_exec.first.return_value = None
            mock_session.exec.return_value = mock_exec

            result = get_task_by_id(mock_session, 999, 1)

            assert result is None


def test_update_task_success(mock_session, sample_task):
    """Test successful task update"""
    with patch('src.services.task_service.get_task_by_id') as mock_get_task:
        mock_get_task.return_value = sample_task

        task_update = TaskUpdate(title="Updated Task")

        result = update_task(mock_session, 1, 1, task_update)

        assert result == sample_task
        assert result.title == "Updated Task"
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()


def test_update_task_not_found(mock_session):
    """Test task update when task doesn't exist"""
    with patch('src.services.task_service.get_task_by_id') as mock_get_task:
        mock_get_task.return_value = None

        task_update = TaskUpdate(title="Updated Task")

        result = update_task(mock_session, 999, 1, task_update)

        assert result is None


def test_delete_task_success(mock_session, sample_task):
    """Test successful task deletion"""
    with patch('src.services.task_service.get_task_by_id') as mock_get_task:
        mock_get_task.return_value = sample_task

        mock_session.delete = Mock()

        result = delete_task(mock_session, 1, 1)

        assert result is True
        mock_session.delete.assert_called_once()


def test_delete_task_not_found(mock_session):
    """Test task deletion when task doesn't exist"""
    with patch('src.services.task_service.get_task_by_id') as mock_get_task:
        mock_get_task.return_value = None

        result = delete_task(mock_session, 999, 1)

        assert result is False


def test_toggle_task_completion_success(mock_session, sample_task):
    """Test successful task completion toggle"""
    with patch('src.services.task_service.get_task_by_id') as mock_get_task:
        sample_task.status = "pending"
        mock_get_task.return_value = sample_task

        result = toggle_task_completion(mock_session, 1, 1)

        assert result == sample_task
        assert result.status == "completed"
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()


if __name__ == "__main__":
    pytest.main()