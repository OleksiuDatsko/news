from sqlalchemy import Column, Text
from sqlalchemy.orm import relationship
from models.base import BaseModel


class Author(BaseModel):
    __tablename__ = "authors"
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    bio = Column(Text)

    articles = relationship("Article", back_populates="author")
    newsletter_subs = relationship("NewsletterSubscription", back_populates="author")
