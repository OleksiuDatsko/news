from sqlalchemy import (
    Column,
    Text,
    Boolean,
    BigInteger,
    DateTime,
    ForeignKey,
    Numeric,
    func,
)
from sqlalchemy.orm import relationship, backref, remote
from models.base import BaseModel


class Article(BaseModel):
    __tablename__ = "articles"
    author_id = Column(BigInteger, ForeignKey("authors.id"), nullable=False)
    category_id = Column(BigInteger, ForeignKey("categories.id"))
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    status = Column(Text, nullable=False, default="draft")
    is_exclusive = Column(Boolean, nullable=False, default=False)
    is_breaking = Column(Boolean, nullable=False, default=False)
    views_count = Column(BigInteger, nullable=False, default=0)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    author = relationship("Author", back_populates="articles")
    category = relationship("Category", back_populates="articles")
    keywords = relationship("ArticleKeyword", back_populates="article")
    views = relationship("ArticleView", back_populates="article")
    comments = relationship("Comment", back_populates="article")
    interactions = relationship("ArticleInteraction", back_populates="article")
    notifications = relationship("Notification", back_populates="article")

    def to_dict(self, metadata: bool | None = None):
        if metadata:
            return {
                "id": self.id,
                "author": self.author.to_dict(),
                "category": self.category.to_dict() if self.category else None,
                "title": self.title,
                "status": self.status,
                "is_exclusive": self.is_exclusive,
                "is_breaking": self.is_breaking,
                "views_count": self.views_count,
                "created_at": self.created_at.isoformat(),
                "keywords": [keyword.keyword for keyword in self.keywords],
            }
        return {
            "id": self.id,
            "author": self.author.to_dict(),
            "category": self.category.to_dict() if self.category else None,
            "title": self.title,
            "content": self.content,
            "status": self.status,
            "is_exclusive": self.is_exclusive,
            "is_breaking": self.is_breaking,
            "views_count": self.views_count,
            "created_at": self.created_at.isoformat(),
            "keywords": [keyword.keyword for keyword in self.keywords],
        }


class ArticleKeyword(BaseModel):
    __tablename__ = "article_keywords"
    article_id = Column(BigInteger, ForeignKey("articles.id"), nullable=False)
    keyword = Column(Text, nullable=False)
    article = relationship("Article", back_populates="keywords")


class ArticleView(BaseModel):
    __tablename__ = "article_views"
    article_id = Column(BigInteger, ForeignKey("articles.id"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    session_id = Column(Text)
    ip_address = Column(Text)
    viewed_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    article = relationship("Article", back_populates="views")
    user = relationship("User", back_populates="article_views")


class Comment(BaseModel):
    __tablename__ = "comments"
    article_id = Column(BigInteger, ForeignKey("articles.id"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    text = Column(Text, nullable=False)
    status = Column(Text, nullable=False, default="active")
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    article = relationship("Article", back_populates="comments")
    user = relationship("User", back_populates="comments")

    def to_dict(self):
        return {
            "id": self.id,
            "article_id": self.article_id,
            "user": (
                {"id": self.user.id, "username": self.user.username}
                if self.user
                else None
            ),
            "text": self.text,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }


class ArticleInteraction(BaseModel):
    __tablename__ = "article_interactions"
    article_id = Column(BigInteger, ForeignKey("articles.id"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    interaction_type = Column(Text, nullable=False)  # saved, liked, disliked
    value = Column(Numeric)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    article = relationship("Article", back_populates="interactions")
    user = relationship("User", back_populates="interactions")
