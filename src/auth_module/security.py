from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

# Password hashing configuration
# Simple password hashing for testing (avoiding bcrypt issues)
import hashlib

# JWT configuration
SECRET_KEY = "super-secret-key-for-test"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # For testing purposes, use simple SHA256 hash
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

def get_password_hash(password: str) -> str:
    # For testing purposes, use simple SHA256 hash
    return hashlib.sha256(password.encode()).hexdigest()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    # Only add expiration if not already present in data
    if "exp" not in to_encode:
        # Convert datetime to timestamp (integer) before passing to JWT
        to_encode["exp"] = int(expire.timestamp())
    else:
        # If exp is already present and it's a datetime object, convert to UTC timestamp
        if isinstance(to_encode["exp"], datetime):
            to_encode["exp"] = int(to_encode["exp"].timestamp())
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    try:
        # Skip expiration validation during decoding, check manually
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={'verify_exp': False})
        # Check if token is expired (exp is in seconds since epoch)
        exp_timestamp = payload.get("exp")
        if exp_timestamp and datetime.utcnow().timestamp() > float(exp_timestamp):
            return None
        return payload
    except JWTError:
        return None