from sqlalchemy import Column, DateTime, Text, func
from models.base import BaseModel


class Admin(BaseModel):
    __tablename__ = "admins"

    email = Column(Text, unique=True, nullable=False)
    password = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "created_at": self.created_at,
        }

    @property
    def is_admin(self):
        return True
