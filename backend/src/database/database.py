from sqlmodel import create_engine
from sqlalchemy.pool import QueuePool
import os
from dotenv import load_dotenv

# Import all models to register them with SQLModel
from ..models.user import User
from ..models.task import Task
from ..models.task_tag import TaskTag
from ..models.recurrence import RecurrencePattern

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", os.getenv("NEON_DATABASE_URL", "postgresql://user:password@localhost/todo_app"))

# Create the engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=300,
)