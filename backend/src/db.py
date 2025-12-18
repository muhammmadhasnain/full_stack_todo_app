from sqlmodel import create_engine, Session
from .config import settings
from .models.user import User
from .models.task import Task
from .models.recurrence import RecurrencePattern
from .models.task_tag import TaskTag

# Create engine
engine = create_engine(settings.NEON_DATABASE_URL, echo=True)


def get_session():
    """Get database session"""
    with Session(engine) as session:
        yield session