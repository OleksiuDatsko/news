from repositories.repositories import BaseRepository
from models.category import Category
from sqlalchemy.orm import Session


class CategoryRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(db_session, Category)
