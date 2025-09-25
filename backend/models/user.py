from sqlalchemy import JSON, Column, DateTime, Text, func
from sqlalchemy.orm import relationship
from models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    email = Column(Text, unique=True, nullable=False)
    password = Column(Text, nullable=False)
    username = Column(Text, unique=True, nullable=False)
    role = Column(Text, nullable=False, default="free")
    preferences = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # relationships
    articles = relationship("Article", back_populates="author")
    article_views = relationship("ArticleView", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    interactions = relationship("ArticleInteraction", back_populates="user")
    ad_views = relationship("AdView", back_populates="user")
    subscriptions = relationship("UserSubscriptionPlan", back_populates="user")
    newsletter_subs = relationship("NewsletterSubscription", back_populates="user")
    notifications = relationship("Notification", back_populates="user")