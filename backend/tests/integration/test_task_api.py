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


def test_create_task_success(client: TestClient):
    """Test successful task creation"""
    # First register and login a user to get token
    register_data = {
        "email": "taskuser@example.com",
        "password": "password123"
    }
    register_response = client.post("/api/auth/register", json=register_data)
    assert register_response.status_code == 200

    login_data = {
        "email": "taskuser@example.com",
        "password": "password123"
    }
    login_response = client.post("/api/auth/login", json=login_data)
    assert login_response.status_code == 200

    data = login_response.json()
    access_token = data["access_token"]
    user_id = data["user"]["id"]

    # Create a task
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "priority": "medium",
        "user_id": user_id
    }

    response = client.post(f"/api/{user_id}/tasks",
                          json=task_data,
                          headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    task = response.json()

    assert task["title"] == "Test Task"
    assert task["description"] == "Test Description"
    assert task["priority"] == "medium"
    assert task["status"] == "pending"
    assert task["user_id"] == user_id


def test_get_task_list_success(client: TestClient):
    """Test successful retrieval of task list"""
    # Register and login user
    register_data = {
        "email": "listuser@example.com",
        "password": "password123"
    }
    register_response = client.post("/api/auth/register", json=register_data)
    assert register_response.status_code == 200

    login_data = {
        "email": "listuser@example.com",
        "password": "password123"
    }
    login_response = client.post("/api/auth/login", json=login_data)
    assert login_response.status_code == 200

    data = login_response.json()
    access_token = data["access_token"]
    user_id = data["user"]["id"]

    # Create a task first
    task_data = {
        "title": "List Test Task",
        "description": "List Test Description",
        "priority": "high",
        "user_id": user_id
    }
    create_response = client.post(f"/api/{user_id}/tasks",
                                json=task_data,
                                headers={"Authorization": f"Bearer {access_token}"})
    assert create_response.status_code == 200

    # Get task list
    response = client.get(f"/api/{user_id}/tasks",
                         headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    task_list = response.json()

    assert "tasks" in task_list
    assert "total" in task_list
    assert len(task_list["tasks"]) >= 1
    assert task_list["total"] >= 1

    # Check that the created task is in the list
    task_found = False
    for task in task_list["tasks"]:
        if task["title"] == "List Test Task":
            task_found = True
            break
    assert task_found


def test_get_specific_task_success(client: TestClient):
    """Test successful retrieval of a specific task"""
    # Register and login user
    register_data = {
        "email": "specificuser@example.com",
        "password": "password123"
    }
    register_response = client.post("/api/auth/register", json=register_data)
    assert register_response.status_code == 200

    login_data = {
        "email": "specificuser@example.com",
        "password": "password123"
    }
    login_response = client.post("/api/auth/login", json=login_data)
    assert login_response.status_code == 200

    data = login_response.json()
    access_token = data["access_token"]
    user_id = data["user"]["id"]

    # Create a task
    task_data = {
        "title": "Specific Test Task",
        "description": "Specific Test Description",
        "priority": "low",
        "user_id": user_id
    }
    create_response = client.post(f"/api/{user_id}/tasks",
                                json=task_data,
                                headers={"Authorization": f"Bearer {access_token}"})
    assert create_response.status_code == 200

    created_task = create_response.json()
    task_id = created_task["id"]

    # Get the specific task
    response = client.get(f"/api/{user_id}/tasks/{task_id}",
                         headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    task = response.json()

    assert task["id"] == task_id
    assert task["title"] == "Specific Test Task"
    assert task["description"] == "Specific Test Description"


def test_update_task_success(client: TestClient):
    """Test successful task update"""
    # Register and login user
    register_data = {
        "email": "updateuser@example.com",
        "password": "password123"
    }
    register_response = client.post("/api/auth/register", json=register_data)
    assert register_response.status_code == 200

    login_data = {
        "email": "updateuser@example.com",
        "password": "password123"
    }
    login_response = client.post("/api/auth/login", json=login_data)
    assert login_response.status_code == 200

    data = login_response.json()
    access_token = data["access_token"]
    user_id = data["user"]["id"]

    # Create a task
    task_data = {
        "title": "Update Test Task",
        "description": "Update Test Description",
        "priority": "medium",
        "user_id": user_id
    }
    create_response = client.post(f"/api/{user_id}/tasks",
                                json=task_data,
                                headers={"Authorization": f"Bearer {access_token}"})
    assert create_response.status_code == 200

    created_task = create_response.json()
    task_id = created_task["id"]

    # Update the task
    update_data = {
        "title": "Updated Task Title",
        "description": "Updated Task Description",
        "priority": "high"
    }
    response = client.put(f"/api/{user_id}/tasks/{task_id}",
                         json=update_data,
                         headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    updated_task = response.json()

    assert updated_task["id"] == task_id
    assert updated_task["title"] == "Updated Task Title"
    assert updated_task["description"] == "Updated Task Description"
    assert updated_task["priority"] == "high"


def test_delete_task_success(client: TestClient):
    """Test successful task deletion"""
    # Register and login user
    register_data = {
        "email": "deleteuser@example.com",
        "password": "password123"
    }
    register_response = client.post("/api/auth/register", json=register_data)
    assert register_response.status_code == 200

    login_data = {
        "email": "deleteuser@example.com",
        "password": "password123"
    }
    login_response = client.post("/api/auth/login", json=login_data)
    assert login_response.status_code == 200

    data = login_response.json()
    access_token = data["access_token"]
    user_id = data["user"]["id"]

    # Create a task
    task_data = {
        "title": "Delete Test Task",
        "description": "Delete Test Description",
        "priority": "medium",
        "user_id": user_id
    }
    create_response = client.post(f"/api/{user_id}/tasks",
                                json=task_data,
                                headers={"Authorization": f"Bearer {access_token}"})
    assert create_response.status_code == 200

    created_task = create_response.json()
    task_id = created_task["id"]

    # Delete the task
    response = client.delete(f"/api/{user_id}/tasks/{task_id}",
                            headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200

    # Verify the task is deleted by trying to get it
    get_response = client.get(f"/api/{user_id}/tasks/{task_id}",
                             headers={"Authorization": f"Bearer {access_token}"})
    assert get_response.status_code == 404


def test_toggle_task_completion_success(client: TestClient):
    """Test successful task completion toggle"""
    # Register and login user
    register_data = {
        "email": "toggleuser@example.com",
        "password": "password123"
    }
    register_response = client.post("/api/auth/register", json=register_data)
    assert register_response.status_code == 200

    login_data = {
        "email": "toggleuser@example.com",
        "password": "password123"
    }
    login_response = client.post("/api/auth/login", json=login_data)
    assert login_response.status_code == 200

    data = login_response.json()
    access_token = data["access_token"]
    user_id = data["user"]["id"]

    # Create a task
    task_data = {
        "title": "Toggle Test Task",
        "description": "Toggle Test Description",
        "priority": "medium",
        "user_id": user_id
    }
    create_response = client.post(f"/api/{user_id}/tasks",
                                json=task_data,
                                headers={"Authorization": f"Bearer {access_token}"})
    assert create_response.status_code == 200

    created_task = create_response.json()
    task_id = created_task["id"]

    # Toggle task completion
    response = client.patch(f"/api/{user_id}/tasks/{task_id}/complete",
                           headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    toggled_task = response.json()

    assert toggled_task["id"] == task_id
    assert toggled_task["status"] == "completed"


if __name__ == "__main__":
    pytest.main()