from sqlalchemy import Column, Text, JSON, BigInteger, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from models.base import BaseModel

class NewsletterSubscription(BaseModel):
    __tablename__ = "newsletter_subscriptions"
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    author_id = Column(BigInteger, ForeignKey("authors.id"))
    type = Column(Text, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    props = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    user = relationship("User", back_populates="newsletter_subs")
    author = relationship("Author", back_populates="newsletter_subs")
