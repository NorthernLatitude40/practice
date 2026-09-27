"""
Unit tests for Pydantic data models.
"""
import pytest
from pydantic import ValidationError

from auth_module.models import (
    UserCreate,
    UserLogin,
    Token,
    UserResponse,
    UserRole
)


class TestUserCreateModel:
    """Test UserCreate model validation."""

    def test_user_create_valid_email(self):
        """Should accept valid email formats."""
        valid_emails = [
            "user@example.com",
            "first.last@sub.domain.com",
            "user+tag@example.org",
            "user-name@example.net"
        ]
        for email in valid_emails:
            user = UserCreate(email=email, password="test123", role=UserRole.USER)
            assert user.email == email

    def test_user_create_invalid_email(self):
        """Should reject invalid email formats."""
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "user@",
            "user..name@example.com"
        ]
        for email in invalid_emails:
            with pytest.raises(ValidationError):
                UserCreate(email=email, password="test123", role=UserRole.USER)

    def test_user_create_default_role(self):
        """Should use USER as default role."""
        user = UserCreate(email="test@example.com", password="test123")
        assert user.role == UserRole.USER

    def test_user_create_admin_role(self):
        """Should accept ADMIN role."""
        user = UserCreate(
            email="admin@example.com", 
            password="test123", 
            role=UserRole.ADMIN
        )
        assert user.role == UserRole.ADMIN

    def test_user_create_password_field(self):
        """Should store password field."""
        user = UserCreate(email="test@example.com", password="mypassword", role=UserRole.USER)
        assert user.password == "mypassword"


class TestUserLoginModel:
    """Test UserLogin model validation."""

    def test_user_login_required_fields(self):
        """Should require email and password."""
        # Valid login
        login = UserLogin(email="test@example.com", password="password123")
        assert login.email == "test@example.com"
        assert login.password == "password123"

    def test_user_login_email_validation(self):
        """Should validate email format."""
        with pytest.raises(ValidationError):
            UserLogin(email="invalid-email", password="password123")


class TestTokenModel:
    """Test Token model."""

    def test_token_defaults(self):
        """Should use correct default values."""
        token = Token(access_token="test-token")
        assert token.token_type == "bearer"

    def test_token_custom_type(self):
        """Should accept custom token type."""
        token = Token(access_token="test-token", token_type="custom")
        assert token.token_type == "custom"


class TestUserResponseModel:
    """Test UserResponse model."""

    def test_user_response_serialization(self):
        """Should serialize to correct format."""
        response = UserResponse(email="test@example.com", role=UserRole.ADMIN)
        data = response.dict()
        assert data["email"] == "test@example.com"
        assert data["role"] == "admin"

    def test_user_response_with_user_role(self):
        """Should handle USER role correctly."""
        response = UserResponse(email="user@example.com", role=UserRole.USER)
        data = response.dict()
        assert data["role"] == "user"

    def test_user_response_json_method(self):
        """Should have working json() method."""
        response = UserResponse(email="test@example.com", role=UserRole.USER)
        json_data = response.json()
        assert "email" in json_data
        assert "role" in json_data


class TestUserRoleEnum:
    """Test UserRole enum."""

    def test_user_role_values(self):
        """Should have correct role values."""
        assert UserRole.USER.value == "user"
        assert UserRole.ADMIN.value == "admin"

    def test_user_role_from_string(self):
        """Should create enum from string value."""
        user_role = UserRole("user")
        admin_role = UserRole("admin")
        assert user_role == UserRole.USER
        assert admin_role == UserRole.ADMIN

    def test_user_role_iteration(self):
        """Should iterate through all roles."""
        roles = list(UserRole)
        assert len(roles) == 2
        assert UserRole.USER in roles
        assert UserRole.ADMIN in roles