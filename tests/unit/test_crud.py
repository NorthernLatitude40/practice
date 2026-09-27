"""
Unit tests for CRUD operations.
"""
import pytest

from auth_module.crud import (
    get_user_by_email,
    create_user,
    get_users,
    create_initial_test_data
)
from auth_module.schemas import DBUser
from auth_module.models import UserCreate, UserRole


class TestCRUDOperations:
    """Test CRUD operations with database."""

    def test_get_user_by_email_exists(self, clean_db_session):
        """Should return user when email exists in database."""
        # Setup: Create a test user in database
        test_user = DBUser(
            email="test@example.com", 
            hashed_password="hashed123", 
            role="user"
        )
        clean_db_session.add(test_user)
        clean_db_session.commit()

        # Test
        result = get_user_by_email(clean_db_session, "test@example.com")
        assert result is not None
        assert result.email == "test@example.com"

    def test_get_user_by_email_not_exists(self, db_session):
        """Should return None when email doesn't exist."""
        result = get_user_by_email(db_session, "nonexistent@example.com")
        assert result is None

    def test_create_user_success(self, clean_db_session):
        """Should successfully create and return user."""
        user_data = UserCreate(
            email="new@example.com", 
            password="testpass", 
            role=UserRole.USER
        )
        result = create_user(clean_db_session, user_data)

        assert result is not None
        assert result.email == "new@example.com"
        assert result.id > 0  # Auto-incremented ID

    def test_create_user_with_admin_role(self, clean_db_session):
        """Should create user with admin role."""
        user_data = UserCreate(
            email="admin@example.com", 
            password="adminpass", 
            role=UserRole.ADMIN
        )
        result = create_user(clean_db_session, user_data)

        assert result is not None
        assert result.role == "admin"

    def test_get_users_pagination(self, clean_db_session):
        """Should return correct number of users based on pagination."""
        # Setup: Create multiple users
        for i in range(5):
            user = DBUser(
                email=f"user{i}@example.com", 
                hashed_password="hashed", 
                role="user"
            )
            clean_db_session.add(user)
        clean_db_session.commit()

        # Test: Get first 2 users
        result = get_users(clean_db_session, skip=0, limit=2)
        assert len(result) == 2

        # Test: Get next 2 users
        result = get_users(clean_db_session, skip=2, limit=2)
        assert len(result) == 2

    def test_get_users_empty_database(self, clean_db_session):
        """Should return empty list for empty database."""
        result = get_users(clean_db_session, skip=0, limit=10)
        assert len(result) == 0

    def test_create_initial_test_data_no_duplicates(self, clean_db_session):
        """Should not create duplicate users if they already exist."""
        # Setup: Create existing user
        existing = DBUser(
            email="user@example.com", 
            hashed_password="hashed", 
            role="user"
        )
        clean_db_session.add(existing)
        clean_db_session.commit()

        # Test: Should not create duplicate
        initial_count = len(get_users(clean_db_session))
        create_initial_test_data(clean_db_session)
        final_count = len(get_users(clean_db_session))
        assert final_count == initial_count  # No new users created

    def test_create_initial_test_data_creates_new_users(self, clean_db_session):
        """Should create new test users when they don't exist."""
        # Test: Should create both user and admin
        initial_count = len(get_users(clean_db_session))
        create_initial_test_data(clean_db_session)
        final_count = len(get_users(clean_db_session))
        assert final_count == initial_count + 2  # Two new users created

    def test_get_user_by_email_case_sensitive(self, clean_db_session):
        """Email lookup should be case sensitive."""
        # Setup: Create user with lowercase email
        test_user = DBUser(
            email="test@example.com", 
            hashed_password="hashed123", 
            role="user"
        )
        clean_db_session.add(test_user)
        clean_db_session.commit()

        # Test: Should not find user with different case
        result = get_user_by_email(clean_db_session, "TEST@EXAMPLE.COM")
        assert result is None