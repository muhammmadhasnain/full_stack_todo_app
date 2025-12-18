# Backend Todo App API - Quickstart Guide

## Prerequisites
- Python 3.11+
- uv (or pip)
- PostgreSQL (or access to Neon Serverless PostgreSQL)
- Redis (for background job processing)

## Setup Instructions

### 1. Environment Setup
```bash
# Navigate to backend directory
cd backend

# Install uv if not already installed
pip install uv

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install project dependencies
uv pip install -r requirements.txt
uv pip install -r requirements-dev.txt
```

### 2. Environment Configuration
Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
NEON_DATABASE_URL=your_neon_connection_string
SECRET_KEY=your_jwt_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
REDIS_URL=redis://localhost:6379
```

### 3. Database Setup
```bash
# Run database migrations
cd backend
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 4. Start the Application
```bash
# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Start the FastAPI server
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Start Background Workers (for recurring tasks)
```bash
# In a separate terminal, start Celery worker
celery -A src.main.celery worker --loglevel=info
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user profile

### Tasks
- `GET /api/{user_id}/tasks` - List user's tasks
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion

## Testing
```bash
# Run all tests
pytest

# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run with coverage
pytest --cov=src
```

## Development Commands
```bash
# Format code
black src/

# Lint code
flake8 src/

# Type check
mypy src/

# Run tests with coverage report
pytest --cov=src --cov-report=html
```