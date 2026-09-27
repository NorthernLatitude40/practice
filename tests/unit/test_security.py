"""
Unit tests for security utilities.
"""
import pytest
from datetime import datetime, timedelta

from auth_module.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token
)


class TestPasswordHashing:
    """Test password hashing and verification."""

    def test_password_hash_consistency(self):
        """Same password should always hash to same value."""
        password = "testpassword123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        assert hash1 == hash2

    def test_verify_correct_password(self):
        """Correct password should verify successfully."""
        password = "testpassword123"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True

    def test_verify_incorrect_password(self):
        """Incorrect password should fail verification."""
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = get_password_hash(password)
        assert verify_password(wrong_password, hashed) is False

    def test_empty_password_handling(self):
        """Empty password should hash to specific value."""
        empty_hash = get_password_hash("")
        assert empty_hash == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

    def test_unicode_password_handling(self):
        """Unicode characters in password should be handled correctly."""
        unicode_password = "testパスワード123"
        hashed = get_password_hash(unicode_password)
        assert verify_password(unicode_password, hashed) is True


class TestJWTTokenManagement:
    """Test JWT token creation and decoding."""

    def test_create_and_decode_jwt_token(self):
        """Created token should be decodable with same data."""
        test_data = {"sub": "test@example.com", "role": "user"}
        token = create_access_token(data=test_data)
        decoded = decode_access_token(token)
        assert decoded is not None
        assert decoded["sub"] == "test@example.com"

    def test_expired_token_rejected(self):
        """Token with past expiration should be rejected."""
        expired_data = {
            "sub": "test@example.com", 
            "exp": datetime.utcnow() - timedelta(minutes=60)
        }
        token = create_access_token(data=expired_data)
        decoded = decode_access_token(token)
        assert decoded is None  # Should be rejected as expired

    def test_malformed_token_handling(self):
        """Malformed tokens should return None."""
        malformed_tokens = [
            "notajwt",
            "",
            "invalid.jwt.token",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.invalid",
        ]
        for token in malformed_tokens:
            assert decode_access_token(token) is None

    def test_token_with_additional_claims(self):
        """Token with additional claims should preserve them."""
        test_data = {
            "sub": "test@example.com", 
            "role": "admin",
            "custom_claim": "custom_value"
        }
        token = create_access_token(data=test_data)
        decoded = decode_access_token(token)
        assert decoded is not None
        assert decoded["custom_claim"] == "custom_value"

    def test_empty_token_payload(self):
        """Empty payload should be handled correctly."""
        token = create_access_token(data={})
        decoded = decode_access_token(token)
        assert decoded is not None
        assert "exp" in decoded  # Should have expiration claim