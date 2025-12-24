# Quickstart: Task ID Type Consistency

## Overview
This guide provides the essential steps to implement UUID-based primary keys for Task entities to resolve the critical inconsistency with User model, API schemas, and frontend expectations.

## Prerequisites
- Python 3.11+
- FastAPI, SQLModel, Pydantic
- Alembic for database migrations
- PostgreSQL with UUID extension

## Implementation Steps

### 1. Update Task Model
Modify the Task model to use UUID primary key:
```python
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel

class Task(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)
    title: str = Field(max_length=255)
    description: str | None = Field(default=None)
    completed: bool = Field(default=False)
    user_id: UUID = Field(foreign_key="user.id")
```

### 2. Update Task Schemas
Ensure all Task schemas expect UUIDs:
```python
from uuid import UUID
from pydantic import BaseModel

class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: str | None
    completed: bool
    user_id: UUID
```

### 3. Create Database Migration
Generate and implement Alembic migration to convert integer IDs to UUIDs:
```bash
alembic revision --autogenerate -m "convert_task_ids_to_uuid"
alembic upgrade head
```

### 4. Update API Endpoints
Ensure all task endpoints accept and return UUIDs:
- Verify path parameters use UUID type
- Confirm response bodies return UUID IDs
- Update error handling for invalid UUID formats

### 5. Update Service Layer
Modify task service functions to handle UUID parameters:
- Update function signatures to accept UUID parameters
- Ensure database queries work with UUID comparisons
- Maintain proper error handling for UUID operations

## Testing
- Run unit tests to verify model changes
- Execute integration tests for API endpoints
- Validate migration with existing data
- Confirm performance meets requirements (<20% degradation)

## Rollback Plan
If critical issues arise:
1. Revert the database migration
2. Revert model changes
3. Revert API endpoint changes
4. Deploy the reverted version