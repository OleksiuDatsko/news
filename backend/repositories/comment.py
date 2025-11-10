from sqlalchemy.orm import Session
from sqlalchemy import desc
from .repositories import BaseRepository
from models.article import Comment


class CommentRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(db_session, Comment)

    def get_by_article(self, article_id: int, page: int = 1, per_page: int = 10):
        """Отримує коментарі для статті з пагінацією"""
        offset = (page - 1) * per_page
        return (
            self.db_session.query(self.model)
            .filter_by(article_id=article_id, status="active")
            .order_by(desc(self.model.created_at))
            .offset(offset)
            .limit(per_page)
            .all()
        )
