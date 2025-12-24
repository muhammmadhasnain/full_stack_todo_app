from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4


class TaskTagBase(SQLModel):
    task_id: UUID
    tag_name: str = Field(max_length=50)


class TaskTag(TaskTagBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)
    task_id: UUID = Field(foreign_key="task.id", index=True)
    tag_name: str = Field(max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship - using string annotations to avoid circular import
    task: "Task" = Relationship(back_populates="task_tags")


class TaskTagCreate(TaskTagBase):
    task_id: UUID
    tag_name: str


class TaskTagResponse(TaskTagBase):
    id: UUID
    created_at: datetime