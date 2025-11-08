from sqlalchemy import Column, ForeignKey, Integer, Table, Text
from sqlalchemy.orm import relationship
from models.base import Base, BaseModel


author_followers = Table(
    "author_followers",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("author_id", Integer, ForeignKey("authors.id"), primary_key=True),
)


class Author(BaseModel):
    __tablename__ = "authors"
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    bio = Column(Text)

    articles = relationship("Article", back_populates="author")
    newsletter_subs = relationship("NewsletterSubscription", back_populates="author")
    followers = relationship(
        "User",
        secondary=author_followers,
        back_populates="followed_authors",
        lazy="dynamic",
    )

    @property
    def total_articles(self):
        return len(self.articles)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "bio": self.bio,
            "total_articles": self.total_articles,
        }
