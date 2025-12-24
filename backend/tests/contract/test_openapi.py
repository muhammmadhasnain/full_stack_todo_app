import pytest
from fastapi.testclient import TestClient
from fastapi.openapi.utils import get_openapi
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.main import app


def test_openapi_spec_exists():
    """Test that OpenAPI spec is available"""
    client = TestClient(app)
    response = client.get("/openapi.json")

    assert response.status_code == 200

    openapi_spec = response.json()
    assert "openapi" in openapi_spec
    assert "info" in openapi_spec
    assert "paths" in openapi_spec
    assert openapi_spec["openapi"].startswith("3.")


def test_openapi_spec_structure():
    """Test the structure of the OpenAPI spec"""
    client = TestClient(app)
    response = client.get("/openapi.json")
    openapi_spec = response.json()

    # Check required fields
    assert "info" in openapi_spec
    assert "title" in openapi_spec["info"]
    assert "version" in openapi_spec["info"]

    # Check that our API endpoints are documented
    assert "/api/auth/register" in openapi_spec["paths"]
    assert "/api/auth/login" in openapi_spec["paths"]
    assert "/api/auth/me" in openapi_spec["paths"]
    assert "/api/{user_id}/tasks" in openapi_spec["paths"]
    assert "/api/{user_id}/tasks/{task_id}" in openapi_spec["paths"]


def test_register_endpoint_spec():
    """Test that the register endpoint is properly specified"""
    client = TestClient(app)
    response = client.get("/openapi.json")
    openapi_spec = response.json()

    register_path = openapi_spec["paths"]["/api/auth/register"]

    # Check that POST method exists
    assert "post" in register_path

    post_spec = register_path["post"]

    # Check that it has a request body
    assert "requestBody" in post_spec
    assert "content" in post_spec["requestBody"]

    # Check that it has responses defined
    assert "responses" in post_spec
    assert "200" in post_spec["responses"]  # Success response
    assert "400" in post_spec["responses"]  # Error response


def test_login_endpoint_spec():
    """Test that the login endpoint is properly specified"""
    client = TestClient(app)
    response = client.get("/openapi.json")
    openapi_spec = response.json()

    login_path = openapi_spec["paths"]["/api/auth/login"]

    # Check that POST method exists
    assert "post" in login_path

    post_spec = login_path["post"]

    # Check that it has a request body
    assert "requestBody" in post_spec
    assert "content" in post_spec["requestBody"]

    # Check that it has responses defined
    assert "responses" in post_spec
    assert "200" in post_spec["responses"]  # Success response
    assert "401" in post_spec["responses"]  # Unauthorized response


def test_task_endpoints_spec():
    """Test that task endpoints are properly specified"""
    client = TestClient(app)
    response = client.get("/openapi.json")
    openapi_spec = response.json()

    # Check GET /api/{user_id}/tasks
    get_tasks_path = openapi_spec["paths"]["/api/{user_id}/tasks"]
    assert "get" in get_tasks_path
    assert "post" in get_tasks_path  # For creating tasks

    # Check GET /api/{user_id}/tasks/{task_id}
    get_task_path = openapi_spec["paths"]["/api/{user_id}/tasks/{task_id}"]
    assert "get" in get_task_path
    assert "put" in get_task_path
    assert "delete" in get_task_path


def test_openapi_with_fastapi_function():
    """Test OpenAPI spec using FastAPI's get_openapi function"""
    openapi_spec = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        description=app.description,
        routes=app.routes,
    )

    assert openapi_spec["info"]["title"] == "Todo App API"
    assert "paths" in openapi_spec
    assert len(openapi_spec["paths"]) > 0  # Should have at least some paths


def test_api_health_endpoint():
    """Test that health endpoint exists and is documented"""
    client = TestClient(app)

    # Test the endpoint works
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


def test_root_endpoint():
    """Test that root endpoint exists"""
    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


if __name__ == "__main__":
    pytest.main()