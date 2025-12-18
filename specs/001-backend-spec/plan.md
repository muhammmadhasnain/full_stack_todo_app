# Implementation Plan: Backend Todo App API

**Branch**: `001-backend-spec` | **Date**: 2025-12-10 | **Spec**: [specs/001-backend-spec/spec.md](specs/001-backend-spec/spec.md)
**Input**: Feature specification from `/specs/001-backend-spec/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a FastAPI-based backend for the Todo App with JWT authentication using Better Auth, SQLModel for database operations with Neon Serverless PostgreSQL, and full CRUD operations for tasks with support for priority, tags, due dates, recurrence, filtering, and search capabilities. The API will follow REST patterns and enforce user data isolation through JWT token validation.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, SQLModel, Better Auth, PyJWT, Neon PostgreSQL driver, Celery, Redis
**Storage**: Neon Serverless PostgreSQL database with SQLModel ORM
**Testing**: pytest for unit and integration tests
**Target Platform**: Linux server (cloud deployment ready)
**Project Type**: web backend - FastAPI REST API
**Performance Goals**: <500ms API response time, handle 1000+ concurrent users, support 10,000+ tasks per user
**Constraints**: JWT token validation using Better Auth on all endpoints, user data isolation, 99% uptime for task operations

**Authentication Technology**: The system will implement authentication using Better Auth framework with JWT tokens for session management and user verification across all protected endpoints.

**Scale/Scope**: Support 10,000+ tasks per user, handle 1000+ concurrent users, 99.9% accuracy for recurring tasks

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Based on the project constitution:
- ✅ Full-Stack Monorepo Architecture: Backend will be in separate backend/ directory as specified in constitution
- ✅ Spec-Driven Development: Implementation follows detailed spec in specs/ directory
- ✅ JWT-Based Authentication Security: All endpoints will implement JWT token verification using Better Auth
- ✅ Type Safety and Validation: Pydantic models will be used for all API requests and responses
- ✅ Database-First Design: SQLModel will be used as primary ORM with Neon Serverless PostgreSQL

## Project Structure

### Documentation (this feature)

```text
specs/001-backend-spec/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── main.py              # FastAPI application entry point
│   ├── celery_app.py        # Celery application for background tasks
│   ├── models/              # SQLModel database models
│   │   ├── user.py          # User model with authentication fields
│   │   ├── task.py          # Task model with all attributes (title, description, priority, etc.)
│   │   ├── recurrence.py    # Recurrence pattern model
│   │   └── base.py          # Base model configuration
│   ├── schemas/             # Pydantic request/response schemas
│   │   ├── user.py          # User-related schemas (register, login, profile)
│   │   ├── task.py          # Task-related schemas (create, update, filter)
│   │   └── auth.py          # Authentication schemas
│   ├── api/                 # API route definitions
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── tasks.py         # Task CRUD endpoints
│   │   └── deps.py          # Dependency injection utilities
│   ├── services/            # Business logic services
│   │   ├── auth_service.py  # Authentication and JWT handling
│   │   ├── task_service.py  # Task management logic
│   │   ├── recurrence_service.py  # Recurring task logic
│   │   └── user_service.py  # User management logic
│   ├── tasks/               # Background task definitions
│   │   └── recurring_tasks.py  # Celery tasks for recurring task generation
│   ├── database/            # Database configuration and session management
│   │   ├── database.py      # Database connection setup
│   │   └── session.py       # Session management
│   └── utils/               # Utility functions
│       ├── security.py      # Password hashing, token utilities
│       ├── filters.py       # Task filtering and search utilities
│       └── validators.py    # Input validation utilities
├── tests/
│   ├── unit/                # Unit tests for services and utilities
│   │   ├── test_auth.py     # Authentication service tests
│   │   ├── test_tasks.py    # Task service tests
│   │   └── test_models.py   # Model validation tests
│   ├── integration/         # Integration tests for API endpoints
│   │   ├── test_auth_api.py # Authentication API tests
│   │   └── test_task_api.py # Task API tests
│   └── contract/            # Contract tests for API compliance
│       └── test_openapi.py  # OpenAPI specification compliance tests
├── requirements.txt         # Python dependencies
├── requirements-dev.txt     # Development dependencies
└── alembic/                 # Database migration configuration
    ├── env.py
    ├── script.py.mako
    └── versions/            # Migration files
```

**Structure Decision**: Option 2: Web application structure is selected as per constitution. Backend will be implemented in backend/ directory with FastAPI application, SQLModel database models, Pydantic schemas, API routes, business logic services, and comprehensive test suite.

## API Contract Standards

Consistent with the project constitution and feature specification, the following API endpoints will be implemented:

### Task Endpoints
- GET /api/{user_id}/tasks - List all tasks for user
- POST /api/{user_id}/tasks - Create a new task
- GET /api/{user_id}/tasks/{id} - Get task details
- PUT /api/{user_id}/tasks/{id} - Update a task
- DELETE /api/{user_id}/tasks/{id} - Delete a task
- PATCH /api/{user_id}/tasks/{id}/complete - Toggle completion status

### Authentication Endpoints
- POST /api/auth/register - Register a new user
- POST /api/auth/login - Authenticate user and return JWT token
- GET /api/auth/me - Get current authenticated user profile

All endpoints (except authentication endpoints) will require JWT authentication and enforce user data isolation. Proper HTTP status codes will be returned for all responses.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
