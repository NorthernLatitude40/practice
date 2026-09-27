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
    user_exists = get_user_by_email(db, "user@example.com") is not None
    admin_exists = get_user_by_email(db, "admin@example.com") is not None

    # Only create test data if neither user exists
    if not user_exists and not admin_exists:
        # Create test user
        test_user = UserCreate(
            email="user@example.com",
            password="b55c8792d1ce458e279308835f8a97b580263503e76e1998e279703e35ad0c2e",  # testpassword123 SHA256 hashed
            role=UserRole.USER
        )
        create_user(db, test_user)

        # Create test admin
        test_admin = UserCreate(
            email="admin@example.com",
            password="426848eb68bf6aa07212a4070863dbe30d92456cf011e238252ddfd86a247856",  # adminpassword123 SHA256 hashed
            role=UserRole.ADMIN
        )
        create_user(db, test_admin)