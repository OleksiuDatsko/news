from sqlalchemy import Column, Text, Boolean, BigInteger, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from models.base import BaseModel


class Notification(BaseModel):
    __tablename__ = "notifications"
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    article_id = Column(BigInteger, ForeignKey("articles.id"))
    type = Column(Text, nullable=False)
    title = Column(Text)
    message = Column(Text)
    is_read = Column(Boolean, nullable=False, default=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    user = relationship("User", back_populates="notifications")
    article = relationship("Article", back_populates="notifications")
