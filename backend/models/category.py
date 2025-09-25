from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from models.base import BaseModel


class Category(BaseModel):
    __tablename__ = "categories"

    name = Column(Text, nullable=False)
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey("categories.id"))
    is_searchable = Column(Boolean, nullable=False, default=True)

    parent = relationship("Category", remote_side=[BaseModel.id], backref="children")
    articles = relationship("Article", back_populates="category")