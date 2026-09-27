import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from auth_module.main import app, get_db
from auth_module.database import Base
from auth_module.crud import create_initial_test_data

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create test database
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def setup_module(module):
    # Initialize test data
    db = next(override_get_db())
    create_initial_test_data(db)

def teardown_module(module):
    pass

def test_register_new_user():
    response = client.post(
        "/register",
        json={
            "email": "newuser@example.com",
            "password": "shortpass123",  # Short password to avoid bcrypt length limit
            "role": "user"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["role"] == "user"

def test_register_existing_user():
    response = client.post(
        "/register",
        json={
            "email": "user@example.com",  # Existing user
            "password": "testpassword123",
            "role": "user"
        }
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]

def test_login_success():
    # Login with the email that was created in setup_module
    response = client.post(
        "/token",
        data={"username": "user@example.com", "password": "testpassword123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_failure():
    response = client.post(
        "/token",
        data={"username": "user@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401

def test_access_protected_route_without_token():
    response = client.get("/api/v1/profile")
    assert response.status_code == 401

def test_access_protected_route_with_invalid_token():
    response = client.get(
        "/api/v1/profile",
        headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response.status_code == 401

def test_access_user_route_with_valid_token():
    # First get a valid token
    login_response = client.post(
        "/token",
        data={"username": "user@example.com", "password": "testpassword123"}
    )
    token = login_response.json()["access_token"]

    # Now access protected route
    response = client.get(
        "/api/v1/profile",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "user@example.com"
    assert data["role"] == "user"

def test_access_admin_route_as_user():
    # Get user token
    login_response = client.post(
        "/token",
        data={"username": "user@example.com", "password": "testpassword123"}
    )
    token = login_response.json()["access_token"]

    # Try to access admin route as regular user
    response = client.get(
        "/api/v1/admin/dashboard",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403

def test_access_admin_route_as_admin():
    # Get admin token
    login_response = client.post(
        "/token",
        data={"username": "admin@example.com", "password": "adminpassword123"}
    )
    token = login_response.json()["access_token"]

    # Access admin route as admin
    response = client.get(
        "/api/v1/admin/dashboard",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "admin dashboard" in data["message"]