from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from models.base import BaseModel


class Category(BaseModel):
    __tablename__ = "categories"

    name = Column(Text, nullable=False)
    description = Column(Text)
    is_searchable = Column(Boolean, nullable=False, default=True)

    articles = relationship("Article", back_populates="category")
