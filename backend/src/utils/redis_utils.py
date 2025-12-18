import redis
import os
from typing import Optional, Any
from uuid import UUID
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Redis connection settings
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')


def get_redis_connection() -> redis.Redis:
    """
    Get a Redis connection
    """
    try:
        redis_client = redis.from_url(
            REDIS_URL,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
            retry_on_timeout=True
        )
        return redis_client
    except Exception as e:
        print(f"Error connecting to Redis: {e}")
        raise


def set_cache(key: str, value: Any, expire: int = 3600) -> bool:
    """
    Set a value in Redis cache with optional expiration
    """
    try:
        redis_client = get_redis_connection()
        redis_client.setex(key, expire, value)
        return True
    except Exception as e:
        print(f"Error setting cache: {e}")
        return False


def get_cache(key: str) -> Optional[str]:
    """
    Get a value from Redis cache
    """
    try:
        redis_client = get_redis_connection()
        value = redis_client.get(key)
        return value
    except Exception as e:
        print(f"Error getting cache: {e}")
        return None


def delete_cache(key: str) -> bool:
    """
    Delete a value from Redis cache
    """
    try:
        redis_client = get_redis_connection()
        result = redis_client.delete(key)
        return result > 0
    except Exception as e:
        print(f"Error deleting cache: {e}")
        return False


def set_user_session(user_id: UUID, session_data: dict, expire: int = 3600) -> bool:
    """
    Set user session data in Redis
    """
    try:
        redis_client = get_redis_connection()
        key = f"user_session:{user_id}"
        redis_client.hset(key, mapping=session_data)
        redis_client.expire(key, expire)
        return True
    except Exception as e:
        print(f"Error setting user session: {e}")
        return False


def get_user_session(user_id: UUID) -> Optional[dict]:
    """
    Get user session data from Redis
    """
    try:
        redis_client = get_redis_connection()
        key = f"user_session:{user_id}"
        session_data = redis_client.hgetall(key)
        return session_data if session_data else None
    except Exception as e:
        print(f"Error getting user session: {e}")
        return None


def delete_user_session(user_id: UUID) -> bool:
    """
    Delete user session data from Redis
    """
    try:
        redis_client = get_redis_connection()
        key = f"user_session:{user_id}"
        result = redis_client.delete(key)
        return result > 0
    except Exception as e:
        print(f"Error deleting user session: {e}")
        return False


def increment_task_counter(task_id: UUID) -> int:
    """
    Increment a task counter in Redis
    """
    try:
        redis_client = get_redis_connection()
        key = f"task_counter:{task_id}"
        count = redis_client.incr(key)
        # Set expiration for the counter
        redis_client.expire(key, 86400)  # 24 hours
        return count
    except Exception as e:
        print(f"Error incrementing task counter: {e}")
        return 0