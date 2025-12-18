from sqlmodel import Session, create_engine
from typing import Generator
from .database import engine


def get_session() -> Generator[Session, None, None]:
    """Dependency to provide database session for FastAPI endpoints"""
    with Session(engine) as session:
        yield session