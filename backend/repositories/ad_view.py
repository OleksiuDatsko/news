from repositories.repositories import BaseRepository
from models.ad import AdView
from sqlalchemy.orm import Session


class AdViewRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(db_session, AdView)

    def get_views_by_ad(self, ad_id: int):
        return self.get_all_by(ad_id=ad_id)

    def get_views_by_user(self, user_id: int):
        return self.get_all_by(user_id=user_id)
