# Implementation Tasks: Backend Todo App API

## Feature Overview

Implementation of a FastAPI-based backend for the Todo App with JWT authentication using Better Auth, SQLModel for database operations with Neon Serverless PostgreSQL, and full CRUD operations for tasks with support for priority, tags, due dates, recurrence, filtering, and search capabilities.

**User Stories Priority Order**:
- [US1] User Registration and Authentication (P1)
- [US2] Task Management Operations (P1)
- [US3] Task Completion and Filtering (P2)
- [US4] Recurring Tasks Management (P3)

## Phase 1: Setup

### Project Structure and Dependencies
- [ ] T001 Create backend/ directory structure per implementation plan
- [ ] T002 [P] Create backend/src/models/ directory
- [ ] T003 [P] Create backend/src/schemas/ directory
- [ ] T004 [P] Create backend/src/api/ directory
- [ ] T005 [P] Create backend/src/services/ directory
- [ ] T006 [P] Create backend/src/database/ directory
- [ ] T007 [P] Create backend/src/utils/ directory
- [ ] T008 [P] Create backend/tests/unit/ directory
- [ ] T009 [P] Create backend/tests/integration/ directory
- [ ] T010 [P] Create backend/tests/contract/ directory
- [ ] T011 Create requirements.txt with FastAPI, SQLModel, PyJWT, python-multipart, celery, redis, redis-py, celery-beat
- [ ] T012 Create requirements-dev.txt with pytest, pytest-asyncio, httpx, factory-boy
- [ ] T013 Setup alembic directory structure with env.py and script.py.mako

## Phase 2: Foundational Components

### Database Setup
- [ ] T014 Create database engine and session management in backend/src/database/database.py
- [ ] T015 Create session dependency in backend/src/database/session.py
- [ ] T016 Create base SQLModel in backend/src/models/base.py

### Security Utilities
- [ ] T017 Create security utilities in backend/src/utils/security.py (password hashing, JWT handling)
- [ ] T018 Create validators in backend/src/utils/validators.py (input validation functions)

### Application Entry Point
- [ ] T019 Create main FastAPI application in backend/src/main.py with proper configuration

### Background Task Setup
- [ ] T020 Create Celery application configuration in backend/src/celery_app.py with Redis broker
- [ ] T021 Create background task definitions in backend/src/tasks/recurring_tasks.py
- [ ] T022A Configure Redis connection settings in backend/src/config.py
- [ ] T022B Create Redis utility functions for connection management in backend/src/utils/redis_utils.py
- [ ] T022C Set up Celery beat scheduler for periodic recurring task checks
- [ ] T022D Create Docker configuration for Redis in docker-compose.yml
- [ ] T022E Implement error handling and retry logic for background tasks

## Phase 3: [US1] User Registration and Authentication

### User Model and Schemas
- [ ] T022 [US1] Create User model in backend/src/models/user.py with all required fields and constraints
- [ ] T023 [US1] Create user schemas in backend/src/schemas/user.py (UserRegister, UserLogin, UserProfile)
- [ ] T024 [US1] Create auth schemas in backend/src/schemas/auth.py (AuthResponse, Token schemas)

### Authentication Service
- [ ] T025 [US1] Create user service in backend/src/services/user_service.py (registration, retrieval logic)
- [ ] T026 [US1] Create auth service in backend/src/services/auth_service.py (login, token generation, validation)

### Authentication Endpoints
- [ ] T027 [US1] Create authentication endpoints in backend/src/api/auth.py (register, login, get profile)
- [ ] T028 [US1] Create JWT dependency in backend/src/api/deps.py (current user validation)

### US1 Independent Test
- [ ] T029 [US1] Test user registration and login flow with JWT token validation

## Phase 4: [US2] Task Management Operations

### Task Model and Schemas
- [ ] T030 [US2] Create Task model in backend/src/models/task.py with all required fields and relationships
- [ ] T031 [US2] Create TaskTag model in backend/src/models/task_tag.py for task tagging functionality
- [ ] T032 [US2] Create task schemas in backend/src/schemas/task.py (TaskCreate, TaskUpdate, TaskResponse)

### Task Service
- [ ] T033 [US2] Create task service in backend/src/services/task_service.py (CRUD operations with user isolation)

### Task Endpoints
- [ ] T034 [US2] Create task endpoints in backend/src/api/tasks.py (create, read, update, delete)
- [ ] T035 [US2] Add user ID validation to task endpoints for data isolation

### US2 Independent Test
- [ ] T036 [US2] Test full CRUD operations for tasks with user data isolation

## Phase 5: [US3] Task Completion and Filtering

### Task Filtering and Search
- [ ] T037 [US3] Create filtering utilities in backend/src/utils/filters.py (status, priority, due date, tag filters)
- [ ] T038 [US3] Implement keyword search functionality for tasks
- [ ] T039 [US3] Add filtering and search to task service methods

### Task Completion Feature
- [ ] T040 [US3] Add completion toggle endpoint in backend/src/api/tasks.py (PATCH /complete)
- [ ] T041 [US3] Update task service to handle completion status changes

### Enhanced Task Endpoints
- [ ] T042 [US3] Add query parameters support for filtering in task list endpoint
- [ ] T043 [US3] Implement pagination for task endpoints

### US3 Independent Test
- [ ] T044 [US3] Test task completion toggle and filtering/search functionality

## Phase 6: [US4] Recurring Tasks Management

### Recurrence Model and Schemas
- [ ] T045 [US4] Create RecurrencePattern model in backend/src/models/recurrence.py with all required fields
- [ ] T046 [US4] Create recurrence schemas in backend/src/schemas/task.py (RecurrencePatternCreate, RecurrencePatternResponse)

### Recurrence Service
- [ ] T047 [US4] Create recurrence service in backend/src/services/recurrence_service.py (pattern creation, task generation logic)
- [ ] T048 [US4] Implement recurring task generation logic with background job processing
- [ ] T048A [US4] Create function to schedule recurring task generation in Celery
- [ ] T048B [US4] Implement logic to create new task instances based on recurrence patterns
- [ ] T048C [US4] Add user_id validation to ensure data isolation in background tasks
- [ ] T048D [US4] Implement monitoring and error logging for recurring task generation

### Task Service Updates
- [ ] T049 [US4] Update task service to handle recurring tasks (creation with recurrence pattern)
- [ ] T050 [US4] Add recurring task logic to task creation and update methods

### US4 Independent Test
- [ ] T051 [US4] Test recurring task creation and automatic generation based on patterns

## Phase 7: Polish & Cross-Cutting Concerns

### Error Handling and Validation
- [ ] T052 Add comprehensive error handling with proper HTTP status codes
- [ ] T053 Implement detailed error response schemas
- [ ] T054 Add request validation and sanitization

### Testing
- [ ] T055 [P] Create unit tests for auth service in backend/tests/unit/test_auth.py
- [ ] T056 [P] Create unit tests for task service in backend/tests/unit/test_tasks.py
- [ ] T057 [P] Create unit tests for models in backend/tests/unit/test_models.py
- [ ] T058 [P] Create integration tests for auth endpoints in backend/tests/integration/test_auth_api.py
- [ ] T059 [P] Create integration tests for task endpoints in backend/tests/integration/test_task_api.py
- [ ] T060 Create contract tests for API compliance in backend/tests/contract/test_openapi.py

### Documentation and Configuration
- [ ] T061 Update API documentation and add endpoint examples
- [ ] T062 Create .env example file with all required environment variables
- [ ] T063 Add proper logging configuration
- [ ] T064 Implement request/response logging middleware
- [ ] T065 Add rate limiting for API endpoints
- [ ] T066 Final integration testing and bug fixes

## Dependencies

### User Story Completion Order
1. [US1] User Registration and Authentication (Foundation for all other stories)
2. [US2] Task Management Operations (Depends on US1 for authentication)
3. [US3] Task Completion and Filtering (Depends on US2 for task operations)
4. [US4] Recurring Tasks Management (Depends on US2 for task operations)

### Parallel Execution Opportunities
- Tasks T002-T010 (directory creation) can run in parallel [P]
- Tasks T021, T022 (schema creation) can run in parallel [P]
- Tasks T030, T031 (model creation) can run in parallel [P]
- Tasks T055-T057 (test creation) can run in parallel [P]

## Implementation Strategy

### MVP Scope (US1 + US2)
- Complete user registration and authentication (US1)
- Basic task CRUD operations (US2)
- User data isolation
- This provides a functional todo app with core features

### Incremental Delivery
- After US1: Authentication system ready
- After US2: Full task management available
- After US3: Enhanced task features (completion, filtering)
- After US4: Advanced recurring tasks