from enum import Enum
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.USER

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    email: EmailStr
    role: UserRole

class UserInDB(BaseModel):
    email: EmailStr
    role: str  # Store as string to match database schema
    id: int