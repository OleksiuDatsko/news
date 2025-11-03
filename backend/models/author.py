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
    
    @property
    def total_articles(self):
        return len(self.articles)
    
    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "bio": self.bio,
            "total_articles": self.total_articles,
        }
