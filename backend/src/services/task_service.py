from sqlmodel import Session, select, and_, or_
from typing import List, Optional
from datetime import datetime, date
from uuid import UUID
from ..models.task import Task, TaskCreate, TaskUpdate
from ..models.user import User
from ..schemas.task import TaskFilter


def create_task(session: Session, task_create: TaskCreate) -> Task:
    """Create a new task"""
    # Check if user exists
    user = session.get(User, task_create.user_id)
    if not user:
        raise ValueError("User not found")

    # Create task object
    task = Task(
        title=task_create.title,
        description=task_create.description,
        status=task_create.status,
        priority=task_create.priority,
        due_date=task_create.due_date,
        tags=task_create.tags,
        user_id=task_create.user_id,
        is_recurring=task_create.is_recurring,
        recurrence_pattern=task_create.recurrence_pattern
    )

    # Add to database
    session.add(task)
    session.commit()
    session.refresh(task)

    return task


def get_task_by_id(session: Session, task_id: UUID, user_id: UUID) -> Optional[Task]:
    """Get a task by ID for a specific user"""
    statement = select(Task).where(
        and_(Task.id == task_id, Task.user_id == user_id)
    )
    task = session.exec(statement).first()
    return task


def get_tasks_by_user(
    session: Session,
    user_id: UUID,
    filters: Optional[TaskFilter] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Task]:
    """Get all tasks for a specific user with optional filters"""
    statement = select(Task).where(Task.user_id == user_id)

    # Apply filters if provided
    if filters:
        conditions = []

        if filters.status:
            conditions.append(Task.status == filters.status)

        if filters.priority:
            conditions.append(Task.priority == filters.priority)

        if filters.due_date_from:
            conditions.append(Task.due_date >= filters.due_date_from)

        if filters.due_date_to:
            conditions.append(Task.due_date <= filters.due_date_to)

        if filters.completed is not None:
            if filters.completed:
                conditions.append(Task.status == "completed")
            else:
                conditions.append(Task.status == "pending")

        if conditions:
            statement = statement.where(and_(*conditions))

    # Apply search filter if provided
    if filters and filters.search:
        search_term = f"%{filters.search}%"
        statement = statement.where(
            or_(
                Task.title.ilike(search_term),
                Task.description.ilike(search_term)
            )
        )

    # Apply pagination
    statement = statement.offset(skip).limit(limit)

    tasks = session.exec(statement).all()
    return tasks


def update_task(session: Session, task_id: UUID, user_id: UUID, task_update: TaskUpdate) -> Optional[Task]:
    """Update a task for a specific user"""
    task = get_task_by_id(session, task_id, user_id)
    if not task:
        return None

    # Update fields
    for field, value in task_update.dict(exclude_unset=True).items():
        if hasattr(task, field):
            setattr(task, field, value)

    # Update timestamp
    task.updated_at = datetime.utcnow()

    # If status is being updated, handle completion time
    if task_update.status and task_update.status == "completed" and task.status != "completed":
        task.completed_at = datetime.utcnow()
    elif task_update.status and task_update.status != "completed" and task.status == "completed":
        task.completed_at = None

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


def delete_task(session: Session, task_id: UUID, user_id: UUID) -> bool:
    """Delete a task for a specific user"""
    task = get_task_by_id(session, task_id, user_id)
    if not task:
        return False

    session.delete(task)
    session.commit()
    return True


def toggle_task_completion(session: Session, task_id: UUID, user_id: UUID) -> Optional[Task]:
    """Toggle the completion status of a task"""
    task = get_task_by_id(session, task_id, user_id)
    if not task:
        return None

    # Toggle status
    if task.status == "pending":
        task.status = "completed"
        task.completed_at = datetime.utcnow()
    else:
        task.status = "pending"
        task.completed_at = None

    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


def get_total_task_count(session: Session, user_id: UUID, filters: Optional[TaskFilter] = None) -> int:
    """Get the total count of tasks for a user with optional filters"""
    from sqlalchemy import func

    # Create a count statement
    count_statement = select(func.count(Task.id)).where(Task.user_id == user_id)

    # Apply filters if provided
    if filters:
        conditions = []

        if filters.status:
            conditions.append(Task.status == filters.status)

        if filters.priority:
            conditions.append(Task.priority == filters.priority)

        if filters.due_date_from:
            conditions.append(Task.due_date >= filters.due_date_from)

        if filters.due_date_to:
            conditions.append(Task.due_date <= filters.due_date_to)

        if filters.completed is not None:
            if filters.completed:
                conditions.append(Task.status == "completed")
            else:
                conditions.append(Task.status == "pending")

        if conditions:
            count_statement = count_statement.where(and_(*conditions))

    # Apply search filter if provided
    if filters and filters.search:
        search_term = f"%{filters.search}%"
        count_statement = count_statement.where(
            or_(
                Task.title.ilike(search_term),
                Task.description.ilike(search_term)
            )
        )

    count = session.exec(count_statement).one()
    return count