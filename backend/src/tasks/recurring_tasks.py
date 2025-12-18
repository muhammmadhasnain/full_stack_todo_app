from celery import Celery
from sqlmodel import create_engine, Session
from datetime import datetime, date
from typing import List
from uuid import UUID
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Celery
celery_app = Celery('recurring_tasks')
celery_app.conf.broker_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
celery_app.conf.result_backend = os.getenv('REDIS_URL', 'redis://localhost:6379')

# Import models and services
from backend.src.models.recurrence import RecurrencePattern
from backend.src.models.task import Task
from backend.src.models.user import User
from backend.src.database.database import engine
from backend.src.services.recurrence_service import (
    should_generate_new_task,
    generate_next_task_date,
    create_task_from_recurrence_pattern
)


@celery_app.task
def process_recurring_tasks():
    """
    Background task to check for recurring tasks that need to be generated
    """
    print(f"Processing recurring tasks at {datetime.utcnow()}")

    with Session(engine) as session:
        # Get all recurrence patterns
        patterns = session.query(RecurrencePattern).all()

        for pattern in patterns:
            try:
                # Check if we need to generate a new task based on this pattern
                # This is a simplified implementation - in a real system, you'd want to track
                # when tasks were last generated and compare with the recurrence pattern
                if should_generate_new_task(pattern):
                    # Find tasks associated with this pattern that are pending or completed
                    associated_tasks = session.query(Task).filter(
                        Task.recurrence_pattern_id == pattern.id
                    ).order_by(Task.created_at.desc()).all()

                    # If there are no associated tasks, create the first one
                    # Or if the last task was completed, create a new one
                    if not associated_tasks or associated_tasks[0].status == "completed":
                        original_task = session.query(Task).filter(
                            Task.recurrence_pattern_id == pattern.id
                        ).first()

                        if original_task:
                            new_task = create_task_from_recurrence_pattern(session, pattern, original_task)
                            if new_task:
                                print(f"Created new recurring task: {new_task.id} for pattern: {pattern.id}")
                            else:
                                print(f"Failed to create new recurring task for pattern: {pattern.id}")
            except Exception as e:
                print(f"Error processing pattern {pattern.id}: {str(e)}")
                # Log error but continue processing other patterns
                continue

    return "Recurring tasks processing completed"


@celery_app.task
def generate_recurring_task(task_id: UUID):
    """
    Generate a specific recurring task
    """
    print(f"Generating recurring task for task ID: {task_id}")

    with Session(engine) as session:
        try:
            # Get the original task
            original_task = session.get(Task, task_id)
            if not original_task or not original_task.recurrence_pattern_id:
                print(f"Original task {task_id} not found or not recurring")
                return False

            # Get the recurrence pattern
            pattern = session.get(RecurrencePattern, original_task.recurrence_pattern_id)
            if not pattern:
                print(f"Recurrence pattern not found for task {task_id}")
                return False

            # Create new task based on the pattern
            new_task = create_task_from_recurrence_pattern(session, pattern, original_task)
            if new_task:
                print(f"Successfully created new recurring task: {new_task.id}")
                return True
            else:
                print(f"Failed to create new recurring task from original task {task_id}")
                return False
        except Exception as e:
            print(f"Error generating recurring task {task_id}: {str(e)}")
            return False


# Schedule the recurring task processing to run daily
from celery.schedules import crontab

celery_app.conf.beat_schedule = {
    'process-recurring-tasks-daily': {
        'task': 'backend.src.tasks.recurring_tasks.process_recurring_tasks',
        'schedule': crontab(minute=0, hour=0),  # Run daily at midnight
    },
}