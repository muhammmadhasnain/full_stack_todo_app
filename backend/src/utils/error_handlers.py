from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from typing import Dict, Any
from uuid import UUID
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TodoAppException(HTTPException):
    """Base exception class for Todo App API"""
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)


class UserNotFoundException(TodoAppException):
    """Raised when a user is not found"""
    def __init__(self, user_id: UUID):
        super().__init__(
            detail=f"User with ID {user_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )


class TaskNotFoundException(TodoAppException):
    """Raised when a task is not found"""
    def __init__(self, task_id: UUID):
        super().__init__(
            detail=f"Task with ID {task_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )


class UnauthorizedException(TodoAppException):
    """Raised when a user is not authorized to perform an action"""
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_403_FORBIDDEN
        )


class InvalidCredentialsException(TodoAppException):
    """Raised when invalid credentials are provided"""
    def __init__(self):
        super().__init__(
            detail="Invalid credentials",
            status_code=status.HTTP_401_UNAUTHORIZED
        )


class DuplicateUserException(TodoAppException):
    """Raised when trying to create a duplicate user"""
    def __init__(self, email: str):
        super().__init__(
            detail=f"User with email {email} already exists",
            status_code=status.HTTP_409_CONFLICT
        )


class ValidationErrorException(TodoAppException):
    """Raised when validation fails"""
    def __init__(self, detail: str):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Global HTTP exception handler"""
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "type": "HTTPException",
                "message": str(exc.detail),
                "status_code": exc.status_code
            }
        }
    )


async def validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global validation exception handler"""
    logger.error(f"Validation Exception: {str(exc)}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "type": "ValidationError",
                "message": "Request validation failed",
                "details": str(exc)
            }
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global general exception handler"""
    logger.error(f"General Exception: {str(exc)}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "type": "InternalServerError",
                "message": "An unexpected error occurred",
                "details": str(exc) if __name__ == "__main__" else "Internal server error"
            }
        }
    )


def add_exception_handlers(app):
    """Add exception handlers to FastAPI app"""
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)