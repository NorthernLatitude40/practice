from sqlalchemy import Column, Integer, String
from auth_module.database import Base

class DBUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role
        }