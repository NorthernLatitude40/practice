# Fix Summary: JWT Token Expiration Bug

## Problem

The test `test_expired_token_rejected` was failing because tokens with past expiration times were being incorrectly accepted as valid.

## Root Cause

When a datetime object representing an expiration time was passed in the `data` dictionary to [`create_access_token()`](auth_module/src/auth_module/security.py:24), the JWT library was treating it as a local timezone-aware datetime and converting it to UTC by subtracting the timezone offset (9 hours for Tokyo). This caused:

- Input: Past expiration time (60 minutes ago)
- After JWT encoding/decoding: Future expiration time (due to timezone conversion)
- Result: Token incorrectly accepted as valid

## Solution

Modified [`create_access_token()`](auth_module/src/auth_module/security.py:24) in `auth_module/src/auth_module/security.py`:

```python
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
```

The fix adds a check: if the `exp` field is already present in the data and it's a datetime object, convert it to a UTC timestamp before passing to JWT. This prevents the timezone conversion issue.

## Testing

- All 10 security tests now pass
- Specifically verified that expired tokens are correctly rejected
- No regression in other functionality
