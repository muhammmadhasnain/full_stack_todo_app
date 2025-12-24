from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .api.auth import router as auth_router
from .api.tasks import router as tasks_router
from .utils.error_handlers import add_exception_handlers
from .utils.logging_middleware import setup_logging
from .utils.rate_limiter import rate_limit_check
from .config import settings
import os

# Load environment variables
load_dotenv()

# Create FastAPI app instance
app = FastAPI(
    title="Todo App API",
    description="A FastAPI-based backend for the Todo App with JWT authentication",
    version="1.0.0",
    debug=settings.DEBUG,
)

# Setup logging
setup_logging(app)

# Add exception handlers
add_exception_handlers(app)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL] if settings.FRONTEND_URL else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(tasks_router, prefix="/api", tags=["Tasks"])

@app.get("/")
def read_root():
    return {"message": "Todo App API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running successfully"}