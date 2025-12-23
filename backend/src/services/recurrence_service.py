
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime, date, timedelta
from uuid import UUID
from ..models.recurrence import RecurrencePattern
from ..models.task import Task
from ..models.user import User
from ..schemas.task import RecurrencePatternCreate as RecurrencePatternCreateSchema


def create_recurrence_pattern(
    session: Session,
    recurrence_data: RecurrencePatternCreateSchema
) -> RecurrencePattern:
    """Create a new recurrence pattern"""
    if recurrence_data.end_condition_type == "after_count" and not recurrence_data.end_count:
        raise ValueError("end_count is required when end_condition_type is 'after_count'")

    if recurrence_data.end_condition_type == "on_date" and not recurrence_data.end_date:
        raise ValueError("end_date is required when end_condition_type is 'on_date'")

    if recurrence_data.end_condition_type == "on_date" and recurrence_data.end_date:
        end_date = datetime.strptime(recurrence_data.end_date, "%Y-%m-%d").date()
        if end_date < date.today():
            raise ValueError("end_date must be in the future")

    recurrence_pattern = RecurrencePattern(
        user_id=recurrence_data.user_id,
        pattern_type=recurrence_data.pattern_type,
        interval=recurrence_data.interval,
        end_condition_type=recurrence_data.end_condition_type,
        end_count=recurrence_data.end_count,
        end_date=recurrence_data.end_date
    )

    session.add(recurrence_pattern)
    session.commit()
    session.refresh(recurrence_pattern)

    return recurrence_pattern


def get_recurrence_pattern_by_id(
    session: Session,
    pattern_id: UUID,
    user_id: UUID
) -> Optional[RecurrencePattern]:
    """Get a recurrence pattern by UUID for a specific user"""
    statement = select(RecurrencePattern).where(
        RecurrencePattern.id == pattern_id,
        RecurrencePattern.user_id == user_id
    )
    pattern = session.exec(statement).first()
    return pattern


def update_recurrence_pattern(
    session: Session,
    pattern_id: UUID,
    user_id: UUID,
    **kwargs
) -> Optional[RecurrencePattern]:
    pattern = get_recurrence_pattern_by_id(session, pattern_id, user_id)
    if not pattern:
        return None

    for field, value in kwargs.items():
        if hasattr(pattern, field):
            setattr(pattern, field, value)

    pattern.updated_at = datetime.utcnow()
    session.add(pattern)
    session.commit()
    session.refresh(pattern)

    return pattern


def delete_recurrence_pattern(
    session: Session,
    pattern_id: UUID,
    user_id: UUID
) -> bool:
    pattern = get_recurrence_pattern_by_id(session, pattern_id, user_id)
    if not pattern:
        return False

    session.delete(pattern)
    session.commit()
    return True


def create_task_from_recurrence_pattern(
    session: Session,
    pattern: RecurrencePattern,
    original_task: Task
) -> Optional[Task]:
    """Create a new task instance based on a recurrence pattern"""
    if pattern.end_condition_type == "on_date" and pattern.end_date:
        if date.today() > pattern.end_date:
            return None

    new_task = Task(
        title=original_task.title,
        description=original_task.description,
        status="pending",
        priority=original_task.priority,
        due_date=original_task.due_date,
        user_id=pattern.user_id,  # Use the pattern's user_id directly since it's now UUID
        is_recurring=True,
        recurrence_pattern=original_task.recurrence_pattern  # Copy the recurrence pattern config from original task
    )

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    return new_task
