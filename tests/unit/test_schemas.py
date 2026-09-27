"""
Unit tests for database schemas and additional models.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from auth_module.schemas import DBUser
from auth_module.models import UserInDB, UserRole
from auth_module.database import Base

# Test database setup
# Use in-memory database for unit tests to avoid write permission issues
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create test database
Base.metadata.create_all(bind=engine)

def get_test_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

class TestDBUserSchema:
    """Test DBUser SQLAlchemy schema."""

    def test_db_user_creation(self):
        """Should create DBUser instance with all fields."""
        user = DBUser(
            id=1,
            email="test@example.com",
            hashed_password="hashed123",
            role="user"
        )
        assert user.id == 1
        assert user.email == "test@example.com"
        assert user.hashed_password == "hashed123"
        assert user.role == "user"

    def test_db_user_to_dict(self):
        """Should convert DBUser to dictionary correctly."""
        user = DBUser(
            id=42,
            email="user@example.com",
            hashed_password="secret_hash",
            role="admin"
        )
        result = user.to_dict()
        assert result == {
            "id": 42,
            "email": "user@example.com",
            "role": "admin"
        }
        assert "hashed_password" not in result  # Should not include password

    def test_db_user_to_dict_with_none_values(self):
        """Should handle None values in to_dict()."""
        user = DBUser(
            id=None,
            email="test@example.com",
            hashed_password="hash123",
            role=None
        )
        result = user.to_dict()
        assert result["email"] == "test@example.com"
        # Should include None values as they are
        assert result["role"] is None

class TestUserInDBModel:
    """Test UserInDB Pydantic model."""

    def test_user_in_db_basic_fields(self):
        """Should create UserInDB with required fields."""
        user = UserInDB(
            email="test@example.com",
            role="user",  # String value, not enum
            id=1
        )
        assert user.email == "test@example.com"
        assert user.role == "user"
        assert user.id == 1

    def test_user_in_db_serialization(self):
        """Should serialize to correct format."""
        user = UserInDB(
            email="admin@example.com",
            role="admin",  # String value, not enum
            id=42
        )
        data = user.dict()
        assert data["email"] == "admin@example.com"
        assert data["role"] == "admin"
        assert data["id"] == 42

    def test_user_in_db_json_method(self):
        """Should have working json() method."""
        user = UserInDB(
            email="user@example.com",
            role="user",  # String value, not enum
            id=1
        )
        json_data = user.json()
        assert "email" in json_data
        assert "role" in json_data
        assert "id" in json_data

    def test_user_in_db_role_enum_conversion(self):
        """Should handle UserRole as string."""
        # Test with USER role (as string)
        user1 = UserInDB(
            email="user@example.com",
            role="user",  # String value
            id=1
        )
        assert user1.role == "user"
    
        # Test with ADMIN role (as string)
        user2 = UserInDB(
            email="admin@example.com",
            role="admin",  # String value
            id=2
        )
        assert user2.role == "admin"

class TestDatabaseIntegration:
    """Test database integration scenarios."""

    def test_db_user_persistence(self):
        """Should persist and retrieve DBUser from database."""
        db = next(get_test_db())

        # Create and save user
        new_user = DBUser(
            email="persist_unit@example.com",
            hashed_password="test_hash",
            role="user"
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Retrieve user
        retrieved = db.query(DBUser).filter_by(email="persist_unit@example.com").first()

        assert retrieved is not None
        assert retrieved.email == "persist_unit@example.com"
        assert retrieved.hashed_password == "test_hash"
        assert retrieved.role == "user"
        assert retrieved.id > 0

    

    def test_db_user_default_values(self):
        """Should handle default values correctly."""
        db = next(get_test_db())

        # Create user without specifying id (should auto-increment)
        user = DBUser(
            email="default_unit@example.com",
            hashed_password="hash123",
            role="user"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        assert user.id > 0  # Should have auto-incremented ID
        assert user.email == "default_unit@example.com"

class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_db_user_with_empty_string_fields(self):
        """Should handle empty string fields."""
        user = DBUser(
            id=1,
            email="",  # Empty email
            hashed_password="",
            role=""  # Empty role
        )
        assert user.email == ""
        assert user.hashed_password == ""
        assert user.role == ""

    def test_db_user_to_dict_with_empty_fields(self):
        """Should handle empty fields in to_dict()."""
        user = DBUser(
            id=1,
            email="",
            hashed_password="hash",
            role=""
        )
        result = user.to_dict()
        assert result["email"] == ""
        assert result["role"] == ""

    def test_user_in_db_with_minimal_values(self):
        """Should create UserInDB with minimal valid values."""
        # Test with minimal required fields - role should be a string
        user = UserInDB(
            email="min@example.com",
            role="user",  # String value, not enum
            id=1
        )
        assert user.email == "min@example.com"
        assert user.role == "user"  # Should be string

    def test_user_in_db_with_single_character_email(self):
        """Should handle single character email addresses."""
        user = UserInDB(
            email="a@b.c",  # Minimal valid email
            role=UserRole.USER,
            id=1
        )
        assert user.email == "a@b.c"

    def test_user_in_db_with_max_values(self):
        """Should handle reasonable maximum length values."""
        # Use a valid but long email address (within Pydantic's limits)
        long_email = "a" * 64 + "@example.com"  # Well within limits
        user = UserInDB(
            email=long_email,
            role=UserRole.ADMIN,
            id=999999
        )
        assert len(user.email) == len(long_email)
        assert user.id == 999999