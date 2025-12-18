from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional
from uuid import UUID
from ..database.session import get_session
from ..schemas.task import (
    TaskCreate, TaskUpdate, TaskResponse, TaskFilter, TaskListResponse, RecurrencePatternCreate
)
from ..services.task_service import (
    create_task, get_task_by_id, get_tasks_by_user, update_task, delete_task,
    toggle_task_completion, get_total_task_count
)
from .deps import get_current_user
from ..models.user import User

router = APIRouter()


@router.get("/{user_id}/tasks", response_model=TaskListResponse)
def list_tasks(
    user_id: UUID,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    due_date_from: Optional[str] = Query(None),
    due_date_to: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    completed: Optional[bool] = Query(None)
):
    """List all tasks for a user with optional filters"""
    # Ensure user can only access their own tasks
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these tasks"
        )

    # Create filter object
    filters = TaskFilter(
        status=status,
        priority=priority,
        due_date_from=due_date_from,
        due_date_to=due_date_to,
        search=search,
        completed=completed
    )

    # Get tasks and total count
    tasks = get_tasks_by_user(session, user_id, filters, skip, limit)
    total = get_total_task_count(session, user_id, filters)

    # Convert to response format
    task_responses = []
    for task in tasks:
        task_response = TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            due_date=task.due_date,
            tags=task.tags,  # Add tags field
            user_id=task.user_id,
            created_at=task.created_at,
            updated_at=task.updated_at,
            completed_at=task.completed_at,
            is_recurring=task.is_recurring,
            recurrence_pattern=task.recurrence_pattern  # Add recurrence pattern field
        )
        task_responses.append(task_response)

    return TaskListResponse(tasks=task_responses, total=total)


@router.post("/{user_id}/tasks", response_model=TaskResponse)
def create_task_endpoint(
    user_id: UUID,
    task_create: TaskCreate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new task for a user"""
    # Ensure user can only create tasks for themselves
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )

    # Ensure the task is being created for the correct user
    task_create.user_id = user_id

    try:
        task = create_task(session, task_create)
        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            due_date=task.due_date,
            tags=task.tags,
            user_id=task.user_id,
            created_at=task.created_at,
            updated_at=task.updated_at,
            completed_at=task.completed_at,
            is_recurring=task.is_recurring,
            recurrence_pattern=task.recurrence_pattern
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    user_id: UUID,
    task_id: UUID,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific task for a user"""
    # Ensure user can only access their own tasks
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )

    task = get_task_by_id(session, task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        tags=task.tags,
        user_id=task.user_id,
        created_at=task.created_at,
        updated_at=task.updated_at,
        completed_at=task.completed_at,
        is_recurring=task.is_recurring,
        recurrence_pattern=task.recurrence_pattern
    )


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
def update_task_endpoint(
    user_id: UUID,
    task_id: UUID,
    task_update: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a specific task for a user"""
    # Ensure user can only update their own tasks
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    task = update_task(session, task_id, user_id, task_update)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        tags=task.tags,
        user_id=task.user_id,
        created_at=task.created_at,
        updated_at=task.updated_at,
        completed_at=task.completed_at,
        is_recurring=task.is_recurring,
        recurrence_pattern=task.recurrence_pattern
    )


@router.delete("/{user_id}/tasks/{task_id}")
def delete_task_endpoint(
    user_id: UUID,
    task_id: UUID,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a specific task for a user"""
    # Ensure user can only delete their own tasks
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )

    success = delete_task(session, task_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return {"message": "Task deleted successfully"}


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
def toggle_task_completion_endpoint(
    user_id: UUID,
    task_id: UUID,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Toggle the completion status of a task"""
    # Ensure user can only update their own tasks
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    task = toggle_task_completion(session, task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        tags=task.tags,
        user_id=task.user_id,
        created_at=task.created_at,
        updated_at=task.updated_at,
        completed_at=task.completed_at,
        is_recurring=task.is_recurring,
        recurrence_pattern=task.recurrence_pattern
    )