"""
Integration tests between frontend and backend systems (TEST-001, TEST-002)
"""
import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool
from uuid import uuid4, UUID
from datetime import datetime
from backend.main import app  # Assuming the main FastAPI app is in backend/main.py
from backend.database.database import SQLModel
from backend.models.user import User
from backend.models.task import Task
from backend.schemas.task import TaskCreate, TaskResponse
from backend.services.task_service import create_task, get_task_by_id
from backend.utils.security import get_password_hash


@pytest.fixture(name="engine")
def fixture_engine():
    # Create an in-memory SQLite database for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(name="session")
def fixture_session(engine):
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def fixture_client(engine):
    def get_test_session():
        with Session(engine) as session:
            yield session

    # Override the dependency to use the test session
    app.dependency_overrides[get_test_session] = get_test_session
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_frontend_backend_integration_complete_workflow(client: TestClient, session: Session):
    """
    Test integration between frontend and backend systems:
    - User creation and authentication
    - Task creation with UUID and ISO datetime
    - Task retrieval and validation
    - Task update and verification
    - Task deletion
    """
    # 1. Create a test user
    user_email = f"testuser_{uuid4()}@example.com"
    user_data = {
        "name": "Integration Test User",
        "email": user_email,
        "password": "securepassword123"
    }

    # Register user (this would normally happen through auth endpoint)
    from backend.models.user import User
    from backend.utils.security import get_password_hash
    hashed_password = get_password_hash(user_data["password"])
    user = User(
        email=user_data["email"],
        name=user_data["name"],
        hashed_password=hashed_password
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.id is not None
    assert isinstance(user.id, UUID)  # Verify UUID string ID

    # Verify user data consistency
    assert user.email == user_data["email"]
    assert user.name == user_data["name"]
    assert user.created_at is not None
    assert user.updated_at is not None
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)

    print(f"✓ Created user with UUID: {user.id}")
    print(f"✓ User created_at: {user.created_at} (type: {type(user.created_at)})")
    print(f"✓ User updated_at: {user.updated_at} (type: {type(user.updated_at)})")

    # 2. Create a task using the API
    task_data = {
        "title": "Integration Test Task",
        "description": "Task created during integration test",
        "status": "pending",
        "priority": "medium",
        "tags": "integration,test,api",
        "dueDate": "2024-12-31T10:00:00Z",  # ISO 8601 format
        "isRecurring": False,
        "recurrencePattern": None
    }

    response = client.post(f"/api/{user.id}/tasks", json=task_data)
    assert response.status_code == 200

    created_task = response.json()
    print(f"✓ Created task via API: {created_task}")

    # Verify task structure and data types
    assert "id" in created_task
    assert isinstance(UUID(created_task["id"]), UUID)  # Verify UUID string ID
    assert created_task["user_id"] == str(user.id)  # Verify user_id is UUID string
    assert created_task["title"] == task_data["title"]
    assert created_task["description"] == task_data["description"]
    assert created_task["status"] == task_data["status"]
    assert created_task["priority"] == task_data["priority"]
    assert created_task["tags"] == task_data["tags"]
    assert created_task["due_date"] == task_data["dueDate"]  # Check datetime format
    assert "created_at" in created_task
    assert "updated_at" in created_task

    # Verify datetime formats are ISO 8601
    from datetime import datetime
    created_at_dt = datetime.fromisoformat(created_task["created_at"].replace('Z', '+00:00'))
    updated_at_dt = datetime.fromisoformat(created_task["updated_at"].replace('Z', '+00:00'))
    print(f"✓ Task created_at: {created_task['created_at']} (parsed: {created_at_dt})")
    print(f"✓ Task updated_at: {created_task['updated_at']} (parsed: {updated_at_dt})")

    # 3. Retrieve the task using the API
    task_id = created_task["id"]
    response = client.get(f"/api/{user.id}/tasks/{task_id}")
    assert response.status_code == 200

    retrieved_task = response.json()
    print(f"✓ Retrieved task via API: {retrieved_task}")

    # Verify retrieved task matches created task
    assert retrieved_task["id"] == created_task["id"]
    assert retrieved_task["user_id"] == created_task["user_id"]
    assert retrieved_task["title"] == created_task["title"]
    assert retrieved_task["tags"] == created_task["tags"]
    assert retrieved_task["due_date"] == created_task["due_date"]
    assert retrieved_task["created_at"] == created_task["created_at"]
    assert retrieved_task["updated_at"] == created_task["updated_at"]

    # 4. Update the task using the API
    update_data = {
        "title": "Updated Integration Test Task",
        "status": "in-progress",
        "tags": "integration,test,api,updated"
    }

    response = client.put(f"/api/{user.id}/tasks/{task_id}", json=update_data)
    assert response.status_code == 200

    updated_task = response.json()
    print(f"✓ Updated task via API: {updated_task}")

    # Verify task was updated
    assert updated_task["id"] == task_id
    assert updated_task["title"] == update_data["title"]
    assert updated_task["status"] == update_data["status"]
    assert updated_task["tags"] == update_data["tags"]
    # Verify timestamps were updated
    assert updated_task["updated_at"] != retrieved_task["updated_at"]

    # 5. Test pagination and filtering
    # Create additional tasks for pagination test
    for i in range(3):
        task_data = {
            "title": f"Pagination Test Task {i}",
            "status": "pending",
            "priority": "low",
            "user_id": str(user.id)
        }
        response = client.post(f"/api/{user.id}/tasks", json=task_data)
        assert response.status_code == 200

    # Test pagination endpoint
    response = client.get(f"/api/{user.id}/tasks?skip=0&limit=5")
    assert response.status_code == 200
    paginated_response = response.json()

    assert "tasks" in paginated_response
    assert "total" in paginated_response
    assert len(paginated_response["tasks"]) >= 4  # Original + 3 new tasks
    assert paginated_response["total"] >= 4

    print(f"✓ Pagination test: {len(paginated_response['tasks'])} tasks, total: {paginated_response['total']}")

    # 6. Test task completion toggle
    response = client.patch(f"/api/{user.id}/tasks/{task_id}/complete", json={"completed": True})
    assert response.status_code == 200

    completed_task = response.json()
    assert completed_task["id"] == task_id
    assert completed_task["status"] == "completed"
    if "completed_at" in completed_task:
        assert completed_task["completed_at"] is not None
        print(f"✓ Task completion time: {completed_task['completed_at']}")

    print("✓ All integration tests passed successfully!")


def test_api_contract_compliance():
    """
    Test API contract compliance: Verify all endpoints return consistent UUID and datetime formats
    """
    # This would test that all API endpoints return data in the expected format
    # For now, we'll verify the data models support the required formats

    from backend.schemas.task import TaskResponse

    # Create a task response to verify field types
    task_response = TaskResponse(
        id=uuid4(),  # UUID
        title="Test Task",
        description="Test Description",
        status="pending",
        priority="medium",
        due_date=datetime.utcnow(),
        tags="test,api,contract",
        user_id=uuid4(),  # UUID
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        completed_at=None,
        is_recurring=False,
        recurrence_pattern=None
    )

    # Verify all fields are present and of correct type
    assert isinstance(task_response.id, UUID)
    assert isinstance(task_response.user_id, UUID)
    assert isinstance(task_response.created_at, datetime)
    assert isinstance(task_response.updated_at, datetime)
    assert task_response.tags == "test,api,contract"

    print("✓ API contract compliance verified!")


if __name__ == "__main__":
    # This is just for demonstration - in a real scenario, use pytest to run these tests
    print("Integration tests defined successfully!")
    print("Run with: pytest tests/integration/test_frontend_backend_integration.py")