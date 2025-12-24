"""
Test data consistency for UUID and datetime formats in the task system.
"""
import pytest
from sqlmodel import Session, create_engine
from uuid import UUID
from datetime import datetime
from ..models.task import Task, TaskCreate
from ..models.user import User, UserCreate  
from ..services.task_service import create_task, get_task_by_id
from ..utils.security import get_password_hash


def test_create_task_with_uuid_and_verify_storage_format():
    """Test data consistency: Create task with UUID and verify storage format"""
    # Create an in-memory database for testing
    engine = create_engine("sqlite:///:memory:", echo=True)

    # Create tables
    from ..models.user import User
    from ..models.task import Task
    from ..database.database import User, Task  # This imports and registers the models
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Create a test user
        user_create = UserCreate(
            name="Test User",
            email="test@example.com",
            password="password123"
        )
        hashed_password = get_password_hash(user_create.password)
        user = User(
            email=user_create.email,
            name=user_create.name,
            hashed_password=hashed_password
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        # Verify user has a UUID
        assert isinstance(user.id, UUID), f"User ID should be UUID, got {type(user.id)}"

        # Create a task using the service
        task_create = TaskCreate(
            title="Test Task",
            description="Test Description",
            priority="medium",
            user_id=user.id,  # This should be a UUID
            status="pending"
        )

        created_task = create_task(session, task_create)

        # Verify the task was created with UUID
        assert isinstance(created_task.id, UUID), f"Task ID should be UUID, got {type(created_task.id)}"
        assert isinstance(created_task.user_id, UUID), f"Task user_id should be UUID, got {type(created_task.user_id)}"

        # Verify datetime formats are proper
        assert isinstance(created_task.created_at, datetime), f"created_at should be datetime, got {type(created_task.created_at)}"
        assert isinstance(created_task.updated_at, datetime), f"updated_at should be datetime, got {type(created_task.updated_at)}"

        print(f"✓ Task ID: {created_task.id} (type: {type(created_task.id)})")
        print(f"✓ Task user_id: {created_task.user_id} (type: {type(created_task.user_id)})")
        print(f"✓ Task created_at: {created_task.created_at} (type: {type(created_task.created_at)})")
        print(f"✓ Task updated_at: {created_task.updated_at} (type: {type(created_task.updated_at)})")

        # Verify the UUID is properly formatted
        assert str(created_task.id) == created_task.id.hex, "UUID should be properly formatted"


def test_retrieve_task_and_verify_uuid_datetime_formats():
    """Test data consistency: Retrieve task and verify UUID and datetime formats match storage"""
    # Create an in-memory database for testing
    engine = create_engine("sqlite:///:memory:", echo=True)

    # Create tables
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Create a test user
        user_create = UserCreate(
            name="Test User",
            email="test@example.com",
            password="password123"
        )
        hashed_password = get_password_hash(user_create.password)
        user = User(
            email=user_create.email,
            name=user_create.name,
            hashed_password=hashed_password
        )
        session.add(user)    
        session.commit()
        session.refresh(user)

        # Verify user has a UUID
        assert isinstance(user.id, UUID), f"User ID should be UUID, got {type(user.id)}"

        # Create a task using the service
        task_create = TaskCreate(
            title="Test Task for Retrieval",
            description="Test Description for Retrieval",
            priority="high",
            user_id=user.id,
            status="pending"
        )

        created_task = create_task(session, task_create)

        # Verify the created task has proper formats
        original_task_id = created_task.id
        original_user_id = created_task.user_id
        original_created_at = created_task.created_at
        original_updated_at = created_task.updated_at

        # Retrieve the task using the service
        retrieved_task = get_task_by_id(session, created_task.id, created_task.user_id)

        # Verify the retrieved task exists
        assert retrieved_task is not None, "Task should be retrievable"

        # Verify all formats match between created and retrieved
        assert retrieved_task.id == original_task_id, "Task ID should match"
        assert retrieved_task.user_id == original_user_id, "Task user_id should match"
        assert retrieved_task.created_at == original_created_at, "Task created_at should match"
        assert retrieved_task.updated_at == original_updated_at, "Task updated_at should match"

        # Verify types are still correct on retrieval
        assert isinstance(retrieved_task.id, UUID), f"Retrieved task ID should be UUID, got {type(retrieved_task.id)}"
        assert isinstance(retrieved_task.user_id, UUID), f"Retrieved task user_id should be UUID, got {type(retrieved_task.user_id)}"
        assert isinstance(retrieved_task.created_at, datetime), f"Retrieved created_at should be datetime, got {type(retrieved_task.created_at)}"
        assert isinstance(retrieved_task.updated_at, datetime), f"Retrieved updated_at should be datetime, got {type(retrieved_task.updated_at)}"

        print(f"✓ Retrieved Task ID: {retrieved_task.id} (type: {type(retrieved_task.id)})")
        print(f"✓ Retrieved Task user_id: {retrieved_task.user_id} (type: {type(retrieved_task.user_id)})")
        print(f"✓ Retrieved Task created_at: {retrieved_task.created_at} (type: {type(retrieved_task.created_at)})")
        print(f"✓ Retrieved Task updated_at: {retrieved_task.updated_at} (type: {type(retrieved_task.updated_at)})")


if __name__ == "__main__":
    # Run the tests
    test_create_task_with_uuid_and_verify_storage_format()
    print("✓ Test 1 passed: Create task with UUID and verify storage format")

    test_retrieve_task_and_verify_uuid_datetime_formats()
    print("✓ Test 2 passed: Retrieve task and verify UUID and datetime formats")

    print("\n✓ All consistency tests passed!")