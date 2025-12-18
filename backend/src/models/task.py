from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4
import uuid


class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    status: str = Field(default="pending", regex="^(pending|completed|in-progress|cancelled|on_hold)$")
    priority: str = Field(regex="^(low|medium|high)$")
    due_date: Optional[datetime] = None
    tags: Optional[str] = None  # Comma-separated tags
    is_recurring: bool = Field(default=False)
    recurrence_pattern: Optional[str] = None  # JSON string for recurrence configuration


class Task(TaskBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None)
    status: str = Field(default="pending", regex="^(pending|completed|in-progress|cancelled|on_hold)$")
    priority: str = Field(regex="^(low|medium|high)$")
    due_date: Optional[datetime] = None
    tags: Optional[str] = Field(default=None)  # Comma-separated tags
    is_recurring: bool = Field(default=False)
    recurrence_pattern: Optional[str] = Field(default=None)  # JSON string for recurrence configuration
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

    # Relationships - using string annotations to avoid circular import
    user: "User" = Relationship(back_populates="tasks")
    task_tags: List["TaskTag"] = Relationship(back_populates="task")


class TaskCreate(TaskBase):
    title: str
    priority: str
    user_id: Optional[UUID] = None


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = Field(default=None, regex="^(pending|completed|in-progress|cancelled|on_hold)$")
    priority: Optional[str] = Field(default=None, regex="^(low|medium|high)$")
    due_date: Optional[datetime] = None
    tags: Optional[str] = None  # Comma-separated tags
    is_recurring: Optional[bool] = None
    recurrence_pattern: Optional[str] = None  # JSON string for recurrence configuration
    completed_at: Optional[datetime] = None
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class TaskResponse(TaskBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None