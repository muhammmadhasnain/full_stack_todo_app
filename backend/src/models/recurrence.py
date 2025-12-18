from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID, uuid4


class RecurrencePatternBase(SQLModel):
    user_id: UUID
    pattern_type: str = Field(regex="^(daily|weekly|monthly|yearly)$")
    interval: int = Field(default=1, ge=1)
    end_condition_type: str = Field(regex="^(never|after_count|on_date)$")
    end_count: Optional[int] = Field(default=None, ge=1)
    end_date: Optional[date] = None


class RecurrencePattern(RecurrencePatternBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    pattern_type: str = Field(regex="^(daily|weekly|monthly|yearly)$")
    interval: int = Field(default=1, ge=1)
    end_condition_type: str = Field(regex="^(never|after_count|on_date)$")
    end_count: Optional[int] = Field(default=None, ge=1)
    end_date: Optional[date] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships - using string annotations to avoid circular import
    user: "User" = Relationship(back_populates="recurrence_patterns")


class RecurrencePatternCreate(RecurrencePatternBase):
    user_id: UUID
    pattern_type: str
    interval: int
    end_condition_type: str


class RecurrencePatternResponse(RecurrencePatternBase):
    id: UUID
    created_at: datetime
    updated_at: datetime