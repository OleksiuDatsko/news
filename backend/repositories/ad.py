from repositories.repositories import BaseRepository
from models.ad import Ad
from sqlalchemy.orm import Session


class AdRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(db_session, Ad)
