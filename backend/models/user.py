from sqlalchemy import Column, String, Boolean, Enum, DateTime
from models import BaseModel, TimestampMixin
from enum import Enum as PyEnum

class UserRole(PyEnum):
    GUEST = "guest"
    READER = "reader"
    AUTHOR = "author"
    ADMIN = "admin"

class User(BaseModel, TimestampMixin):
    __tablename__ = 'users'
    
    email = Column(String(120), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    username = Column(String(80), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.READER)
    is_active = Column(Boolean, default=True)
    is_email_verified = Column(Boolean, default=False)
    last_login = Column(DateTime)
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"
