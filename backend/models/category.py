from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from models.base import BaseModel


class Category(BaseModel):
    __tablename__ = "categories"

    name = Column(Text, nullable=False)
    description = Column(Text)
    slug = Column(Text, nullable=False, unique=True)
    is_searchable = Column(Boolean, nullable=False, default=True)

    articles = relationship("Article", back_populates="category")

    __table_args__ = (
        UniqueConstraint('slug', name='uq_categories_slug'),
    )