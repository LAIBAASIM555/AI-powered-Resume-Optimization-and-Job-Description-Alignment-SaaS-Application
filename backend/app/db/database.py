"""
Database connection and session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.config import settings

# PostgreSQL Database Engine
# pool_pre_ping: Check connection before using
# pool_size: Number of connections to keep
# max_overflow: Extra connections allowed
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=settings.DEBUG  # Log SQL queries in debug mode
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Dependency to get database session
def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency for FastAPI routes.
    Yields a session and ensures it's closed after request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

