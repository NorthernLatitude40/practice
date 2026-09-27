from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth_module.database import get_db, Base, engine
from auth_module.models import UserCreate, UserLogin, Token, UserResponse
from auth_module.schemas import DBUser
from auth_module.crud import get_user_by_email, create_user, create_initial_test_data
from auth_module.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token
)
from auth_module.models import UserRole

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception

    user = get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: DBUser = Depends(get_current_user)):
    return current_user

def get_admin_user(current_user: DBUser = Depends(get_current_active_user)):
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

@app.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)

    # Create a new UserCreate object with the hashed password
    db_user = DBUser(email=user.email, hashed_password=hashed_password, role=user.role.value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserResponse(
        email=db_user.email,
        role=UserRole(db_user.role)
    )

@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.email}
    )
    return Token(access_token=access_token, token_type="bearer")

@app.get("/api/v1/profile", response_model=UserResponse)
def read_profile(current_user: DBUser = Depends(get_current_active_user)):
    return UserResponse(
        email=current_user.email,
        role=UserRole(current_user.role)
    )

@app.get("/api/v1/admin/dashboard")
def admin_dashboard(admin_user: DBUser = Depends(get_admin_user)):
    return {"message": "Welcome to the admin dashboard", "user_role": admin_user.role}

# Initialize test data - disabled to avoid bcrypt issues
# db = next(get_db())
# create_initial_test_data(db)