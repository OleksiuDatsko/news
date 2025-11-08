from sqlalchemy import Column, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base import BaseModel

class PushSubscription(BaseModel):
    __tablename__ = "push_subscriptions"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    endpoint = Column(Text, nullable=False, unique=True)
    p256dh = Column(Text, nullable=False)
    auth = Column(Text, nullable=False)

    user = relationship("User", back_populates="push_subscriptions")
