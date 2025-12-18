from fastapi import Request
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware import Middleware
import time
import logging
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log requests and responses
    """
    async def dispatch(self, request: Request, call_next):
        # Log request
        start_time = time.time()

        # Get client info
        client_host = request.client.host if request.client else "unknown"
        client_port = request.client.port if request.client else "unknown"

        # Get request details
        request_method = request.method
        request_url = str(request.url)
        request_headers = dict(request.headers)

        # Skip logging for health checks to reduce noise
        if request.url.path in ["/health", "/"]:
            response = await call_next(request)
            return response

        logger.info(f"Request: {request_method} {request_url} - Client: {client_host}:{client_port}")

        try:
            # Process request
            response = await call_next(request)

            # Calculate processing time
            process_time = time.time() - start_time

            # Log response
            response_status = response.status_code

            logger.info(
                f"Response: {request_method} {request_url} - "
                f"Status: {response_status} - "
                f"Process Time: {process_time:.4f}s"
            )

            # Add process time to response headers
            response.headers["X-Process-Time"] = str(process_time)

            return response

        except Exception as e:
            # Calculate processing time for error case
            process_time = time.time() - start_time

            logger.error(
                f"Error in request: {request_method} {request_url} - "
                f"Error: {str(e)} - "
                f"Process Time: {process_time:.4f}s"
            )

            # Re-raise the exception to be handled by other error handlers
            raise


def setup_logging(app):
    """
    Setup logging for the FastAPI application
    """
    # Add the logging middleware to the app
    app.add_middleware(LoggingMiddleware)

    # Configure logging format
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )