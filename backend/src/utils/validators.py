from typing import Optional
from pydantic import EmailStr, validator
import re


def validate_email_format(email: str) -> bool:
    """Validate email format using regex"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password strength
    Returns (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"

    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit"

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"

    return True, ""


def validate_task_title(title: str) -> tuple[bool, str]:
    """
    Validate task title
    Returns (is_valid, error_message)
    """
    if not title or len(title.strip()) == 0:
        return False, "Title cannot be empty"

    if len(title) > 255:
        return False, "Title cannot exceed 255 characters"

    return True, ""


def validate_priority(priority: str) -> bool:
    """Validate task priority value"""
    valid_priorities = ["low", "medium", "high"]
    return priority.lower() in valid_priorities