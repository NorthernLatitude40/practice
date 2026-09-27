"""
Test fixtures and shared setup for unit tests.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from auth_module.database import Base

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_unit.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create test database
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a new database session for each test."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


@pytest.fixture(scope="function")
def clean_db_session(db_session):
    """Create a clean database session with no data."""
    # Clear all tables in reverse order to handle foreign keys
    for table in reversed(Base.metadata.sorted_tables):
        db_session.execute(table.delete())
    db_session.commit()
    yield db_session