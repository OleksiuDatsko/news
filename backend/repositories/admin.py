from flask import g
from repositories.repositories import BaseRepository
from models.admin import Admin
from sqlalchemy.orm import Session

class AdminRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(db_session, Admin)
