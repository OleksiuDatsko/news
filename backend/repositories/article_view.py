from repositories.repositories import BaseRepository
from models.article import ArticleView
from sqlalchemy.orm import Session


class ArticleViewRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(db_session, ArticleView)

    def get_views_by_article(self, article_id: int):
        return self.get_all_by(article_id=article_id)

    def get_views_by_user(self, user_id: int):
        return self.get_all_by(user_id=user_id)
