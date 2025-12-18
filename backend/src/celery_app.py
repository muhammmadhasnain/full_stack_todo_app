from celery import Celery
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Celery app
celery_app = Celery('todo_app')

# Configure Celery
celery_app.conf.update(
    broker_url=os.getenv('REDIS_URL', 'redis://localhost:6379'),
    result_backend=os.getenv('REDIS_URL', 'redis://localhost:6379'),
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    broker_connection_retry_on_startup=True,
)

# Auto-discover tasks
celery_app.autodiscover_tasks(['backend.src.tasks'])

# Import the beat schedule from recurring tasks
from backend.src.tasks.recurring_tasks import celery_app as recurring_celery_app
celery_app.conf.beat_schedule = recurring_celery_app.conf.beat_schedule

if __name__ == '__main__':
    celery_app.start()