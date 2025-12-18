from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID
from .user import UserProfile


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "pending"
    priority: str
    due_date: Optional[datetime] = None
    tags: Optional[str] = None  # Comma-separated tags
    is_recurring: bool = False
    recurrence_pattern: Optional[dict] = None  # Recurrence configuration


class TaskCreate(TaskBase):
    title: str
    priority: str
    user_id: Optional[UUID] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    tags: Optional[str] = None  # Comma-separated tags
    is_recurring: Optional[bool] = None
    recurrence_pattern: Optional[dict] = None  # Recurrence configuration
    completed_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class TaskResponse(TaskBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    is_recurring: bool = False


class TaskFilter(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date_from: Optional[datetime] = None
    due_date_to: Optional[datetime] = None
    search: Optional[str] = None
    completed: Optional[bool] = None


class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]
    total: int


class RecurrencePatternBase(BaseModel):
    pattern_type: str
    interval: int = 1
    end_condition_type: str
    end_count: Optional[int] = None
    end_date: Optional[date] = None


class RecurrencePatternCreate(RecurrencePatternBase):
    user_id: Optional[UUID] = None


class RecurrencePatternResponse(RecurrencePatternBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime