# from sqlmodel import Session, select
# from typing import List, Optional
# from datetime import datetime, date, timedelta
# from ..models.recurrence import RecurrencePattern, RecurrencePatternCreate
# from ..models.task import Task
# from ..models.user import User
# from ..schemas.task import RecurrencePatternCreate as RecurrencePatternCreateSchema


# def create_recurrence_pattern(
#     session: Session,
#     recurrence_data: RecurrencePatternCreateSchema
# ) -> RecurrencePattern:
#     """Create a new recurrence pattern"""
#     # Validate the recurrence data
#     if recurrence_data.end_condition_type == "after_count" and not recurrence_data.end_count:
#         raise ValueError("end_count is required when end_condition_type is 'after_count'")

#     if recurrence_data.end_condition_type == "on_date" and not recurrence_data.end_date:
#         raise ValueError("end_date is required when end_condition_type is 'on_date'")

#     if recurrence_data.end_condition_type == "on_date" and recurrence_data.end_date:
#         from datetime import datetime
#         end_date = datetime.strptime(recurrence_data.end_date, "%Y-%m-%d").date()
#         if end_date < date.today():
#             raise ValueError("end_date must be in the future")

#     # Create recurrence pattern object
#     recurrence_pattern = RecurrencePattern(
#         user_id=recurrence_data.user_id,
#         pattern_type=recurrence_data.pattern_type,
#         interval=recurrence_data.interval,
#         end_condition_type=recurrence_data.end_condition_type,
#         end_count=recurrence_data.end_count,
#         end_date=recurrence_data.end_date
#     )

#     # Add to database
#     session.add(recurrence_pattern)
#     session.commit()
#     session.refresh(recurrence_pattern)

#     return recurrence_pattern


# def get_recurrence_pattern_by_id(
#     session: Session,
#     pattern_id: int,
#     user_id: int
# ) -> Optional[RecurrencePattern]:
#     """Get a recurrence pattern by ID for a specific user"""
#     statement = select(RecurrencePattern).where(
#         RecurrencePattern.id == pattern_id,
#         RecurrencePattern.user_id == user_id
#     )
#     pattern = session.exec(statement).first()
#     return pattern


# def update_recurrence_pattern(
#     session: Session,
#     pattern_id: int,
#     user_id: int,
#     **kwargs
# ) -> Optional[RecurrencePattern]:
#     """Update a recurrence pattern for a specific user"""
#     pattern = get_recurrence_pattern_by_id(session, pattern_id, user_id)
#     if not pattern:
#         return None

#     # Update fields
#     for field, value in kwargs.items():
#         if hasattr(pattern, field):
#             setattr(pattern, field, value)

#     # Update timestamp
#     pattern.updated_at = datetime.utcnow()

#     session.add(pattern)
#     session.commit()
#     session.refresh(pattern)

#     return pattern


# def delete_recurrence_pattern(
#     session: Session,
#     pattern_id: int,
#     user_id: int
# ) -> bool:
#     """Delete a recurrence pattern for a specific user"""
#     pattern = get_recurrence_pattern_by_id(session, pattern_id, user_id)
#     if not pattern:
#         return False

#     session.delete(pattern)
#     session.commit()
#     return True


# def should_generate_new_task(
#     pattern: RecurrencePattern,
#     last_generated_task_date: Optional[datetime] = None
# ) -> bool:
#     """Check if a new task should be generated based on the recurrence pattern"""
#     if pattern.end_condition_type == "never":
#         return True

#     if pattern.end_condition_type == "on_date" and pattern.end_date:
#         if date.today() > pattern.end_date:
#             return False

#     # For now, we'll just return True - the actual logic for determining
#     # when to generate new tasks would be implemented in the background task
#     return True


# def generate_next_task_date(
#     pattern: RecurrencePattern,
#     current_date: datetime
# ) -> Optional[datetime]:
#     """Calculate the next date when a task should be generated"""
#     if pattern.pattern_type == "daily":
#         return current_date + timedelta(days=pattern.interval)
#     elif pattern.pattern_type == "weekly":
#         return current_date + timedelta(weeks=pattern.interval)
#     elif pattern.pattern_type == "monthly":
#         # For monthly patterns, we'll add the interval in months
#         # This is a simplified approach - in a real implementation,
#         # you'd want to handle month boundaries properly
#         from dateutil.relativedelta import relativedelta
#         return current_date + relativedelta(months=pattern.interval)
#     elif pattern.pattern_type == "yearly":
#         from dateutil.relativedelta import relativedelta
#         return current_date + relativedelta(years=pattern.interval)
#     else:
#         return None


# def create_task_from_recurrence_pattern(
#     session: Session,
#     pattern: RecurrencePattern,
#     original_task: Task
# ) -> Optional[Task]:
#     """Create a new task instance based on a recurrence pattern"""
#     # Check if the pattern has reached its end condition
#     if pattern.end_condition_type == "on_date" and pattern.end_date:
#         if date.today() > pattern.end_date:
#             return None

#     # For now, we'll just create a copy of the original task
#     # In a real implementation, this would be called by the background task
#     # and would check if the task should be created based on the pattern
#     new_task = Task(
#         title=original_task.title,
#         description=original_task.description,
#         status="pending",
#         priority=original_task.priority,
#         due_date=original_task.due_date,
#         user_id=original_task.user_id,
#         is_recurring=True,
#         recurrence_pattern_id=pattern.id
#     )

#     session.add(new_task)
#     session.commit()
#     session.refresh(new_task)

#     return new_task







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
