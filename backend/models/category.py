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

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "slug": self.slug,
            "is_searchable": self.is_searchable,
            "total_articles": len(self.articles),
        }

    __table_args__ = (UniqueConstraint("slug", name="uq_categories_slug"),)
