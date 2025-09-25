from sqlalchemy import Column, Integer

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class BaseModel(Base):
    """Абстрактний базовий клас для всіх моделей"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    def to_dict(self):
        """Конвертує модель у словник"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"
