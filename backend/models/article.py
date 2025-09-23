from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from models import BaseModel, TimestampMixin
from enum import Enum as PyEnum

class ArticleStatus(PyEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class Article(BaseModel, TimestampMixin):
    __tablename__ = 'articles'
    
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    # category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    status = Column(Enum(ArticleStatus), default=ArticleStatus.DRAFT)
    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    is_searchable = Column(Boolean, default=True)
    
    # Relationships
    author = relationship("User", backref="articles")
    # category = relationship("Category", backref="articles") 
    
    def __repr__(self):
        return f"<Article(id={self.id}, title={self.title[:50]})>"
