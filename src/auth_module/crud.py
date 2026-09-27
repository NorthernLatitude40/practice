from sqlalchemy.orm import Session
from auth_module.schemas import DBUser
from auth_module.models import UserCreate, UserRole

def get_user_by_email(db: Session, email: str):
    return db.query(DBUser).filter(DBUser.email == email).first()

def create_user(db: Session, user: UserCreate):
    db_user = DBUser(
        email=user.email,
        hashed_password=user.password,
        role=user.role.value
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DBUser).offset(skip).limit(limit).all()

def create_initial_test_data(db: Session):
    # Check if users already exist to avoid duplicates
    existing_users = get_users(db)

    if not any(user.email == "user@example.com" for user in existing_users):
        # Create test user
        test_user = UserCreate(
            email="user@example.com",
            password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGtGtWm",  # testpassword123 hashed
            role=UserRole.USER
        )
        create_user(db, test_user)

    if not any(user.email == "admin@example.com" for user in existing_users):
        # Create test admin
        test_admin = UserCreate(
            email="admin@example.com",
            password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGtGtWm",  # adminpassword123 hashed
            role=UserRole.ADMIN
        )
        create_user(db, test_admin)