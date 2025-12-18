from fastapi import Request, HTTPException, status
from typing import Dict
import time
from .redis_utils import get_redis_connection, set_cache, get_cache

# Rate limiting configuration
DEFAULT_RATE_LIMIT = 100  # requests per window
DEFAULT_WINDOW = 60  # seconds


class RateLimiter:
    def __init__(self, requests: int = DEFAULT_RATE_LIMIT, window: int = DEFAULT_WINDOW):
        self.requests = requests
        self.window = window

    async def check_rate_limit(self, request: Request) -> bool:
        """
        Check if the request exceeds the rate limit
        Returns True if request is allowed, False otherwise
        """
        # Get client IP address
        client_ip = self.get_client_ip(request)

        # Create key for this client and endpoint
        key = f"rate_limit:{client_ip}:{request.url.path}"

        # Try to get current count and time from Redis
        current_data = get_cache(key)

        if current_data:
            # Parse the data (format: "count:timestamp")
            count_str, timestamp_str = current_data.split(":")
            count = int(count_str)
            timestamp = float(timestamp_str)

            # Check if the window has expired
            if time.time() - timestamp > self.window:
                # Reset the counter
                set_cache(key, f"1:{time.time()}", self.window)
                return True
            else:
                # Check if we're still within the rate limit
                if count >= self.requests:
                    return False
                else:
                    # Increment the counter
                    set_cache(key, f"{count + 1}:{timestamp}", self.window)
                    return True
        else:
            # First request from this client for this endpoint
            set_cache(key, f"1:{time.time()}", self.window)
            return True

    def get_client_ip(self, request: Request) -> str:
        """
        Get the client's IP address from the request
        """
        # Check for forwarded IP headers first (for use behind proxies/load balancers)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        forwarded_host = request.headers.get("X-Forwarded-Host")
        if forwarded_host:
            return forwarded_host

        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        # Fallback to the direct client IP
        return request.client.host if request.client else "unknown"


# Global rate limiter instance
default_limiter = RateLimiter()


async def rate_limit_check(request: Request):
    """
    Dependency to check rate limits
    """
    allowed = await default_limiter.check_rate_limit(request)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded"
        )