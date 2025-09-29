from repositories.repositories import BaseRepository
from models.author import Author
from sqlalchemy.orm import Session


class AuthorRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(db_session, Author)
