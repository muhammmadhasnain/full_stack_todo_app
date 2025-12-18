from src.database.session import engine
from src.models.user import User
from src.models.task import Task
from src.models.task_tag import TaskTag
from src.models.recurrence import RecurrencePattern
from sqlmodel import SQLModel

# Create all tables
print("Creating database tables...")
SQLModel.metadata.create_all(bind=engine)
print("Database tables created successfully!")