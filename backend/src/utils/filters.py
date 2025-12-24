from typing import List, Optional
from sqlmodel import select, and_, or_
from sqlalchemy import func
from backend.src.models.task import Task
from uuid import UUID


def build_task_filter_query(
    user_id: UUID,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    due_date_from: Optional[str] = None,
    due_date_to: Optional[str] = None,
    search: Optional[str] = None,
    completed: Optional[bool] = None
):
    """
    Build a SQLModel query with filters for tasks
    """
    query = select(Task).where(Task.user_id == user_id)

    conditions = []

    if status:
        conditions.append(Task.status == status)

    if priority:
        conditions.append(Task.priority == priority)

    if due_date_from:
        from datetime import datetime
        date_from = datetime.fromisoformat(due_date_from.replace('Z', '+00:00'))
        conditions.append(Task.due_date >= date_from)

    if due_date_to:
        from datetime import datetime
        date_to = datetime.fromisoformat(due_date_to.replace('Z', '+00:00'))
        conditions.append(Task.due_date <= date_to)

    if completed is not None:
        if completed:
            conditions.append(Task.status == "completed")
        else:
            conditions.append(Task.status == "pending")

    if conditions:
        query = query.where(and_(*conditions))

    # Apply search filter if provided
    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                Task.title.ilike(search_term),
                Task.description.ilike(search_term)
            )
        )

    return query


def apply_pagination(query, skip: int = 0, limit: int = 100):
    """
    Apply pagination to a query
    """
    return query.offset(skip).limit(limit)


def filter_tasks_by_status(tasks: List, status: str) -> List:
    """
    Filter tasks by status in memory
    """
    return [task for task in tasks if task.status == status]


def filter_tasks_by_priority(tasks: List, priority: str) -> List:
    """
    Filter tasks by priority in memory
    """
    return [task for task in tasks if task.priority == priority]


def filter_tasks_by_due_date_range(tasks: List, start_date: Optional[str], end_date: Optional[str]) -> List:
    """
    Filter tasks by due date range in memory
    """
    from datetime import datetime

    filtered_tasks = tasks

    if start_date:
        start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        filtered_tasks = [task for task in filtered_tasks if task.due_date and task.due_date >= start]

    if end_date:
        end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        filtered_tasks = [task for task in filtered_tasks if task.due_date and task.due_date <= end]

    return filtered_tasks


def search_tasks(tasks: List, search_term: str) -> List:
    """
    Search tasks by title or description in memory
    """
    search_lower = search_term.lower()
    return [
        task for task in tasks
        if search_lower in task.title.lower() or
        (task.description and search_lower in task.description.lower())
    ]