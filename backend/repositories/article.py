from sqlalchemy import and_, desc, func
from sqlalchemy.orm import Session
from repositories.repositories import BaseRepository
from repositories.interfaces import IArticleRepository
from models.article import Article, ArticleInteraction


class ArticleRepository(BaseRepository, IArticleRepository):
    def __init__(self, db_session: Session):
        super().__init__(db_session, Article)
    
    def get_by_id(self, article_id: int):
        return self.get_by(id=article_id)
    
    def get_all(self, page: int = 1, per_page: int = 10, filters: dict = None):
        query = self.db_session.query(Article)
        
        if filters:
            if filters.get('status'):
                query = query.filter_by(status=filters['status'])
            if filters.get('category_id'):
                query = query.filter_by(category_id=filters['category_id'])
            if filters.get('is_exclusive') is not None:
                query = query.filter_by(is_exclusive=filters['is_exclusive'])
        
        offset = (page - 1) * per_page
        return query.order_by(desc(Article.created_at)).offset(offset).limit(per_page).all()
    
    def save_article(self, user_id: int, article_id: int):
        """Зберігає статтю для користувача"""
        existing = self.db_session.query(ArticleInteraction).filter(
            and_(
                ArticleInteraction.user_id == user_id,
                ArticleInteraction.article_id == article_id,
                ArticleInteraction.interaction_type == 'saved'
            )
        ).first()
        
        if existing:
            existing.value = 1
            existing.created_at = func.now()
        else:
            interaction = ArticleInteraction(
                user_id=user_id,
                article_id=article_id,
                interaction_type='saved',
                value=1
            )
            self.db_session.add(interaction)
        
        self.db_session.commit()
        return True
    
    def unsave_article(self, user_id: int, article_id: int):
        """Прибирає статтю зі збережених"""
        existing = self.db_session.query(ArticleInteraction).filter(
            and_(
                ArticleInteraction.user_id == user_id,
                ArticleInteraction.article_id == article_id,
                ArticleInteraction.interaction_type == 'saved'
            )
        ).first()
        
        if existing:
            self.db_session.delete(existing)
            self.db_session.commit()
        
        return True
    
    def get_saved_articles(self, user_id: int, page: int = 1, per_page: int = 10):
        """Отримує збережені статті користувача"""
        query = self.db_session.query(Article).join(ArticleInteraction).filter(
            and_(
                ArticleInteraction.user_id == user_id,
                ArticleInteraction.interaction_type == 'saved',
                ArticleInteraction.value == 1
            )
        )
        
        offset = (page - 1) * per_page
        return query.order_by(desc(ArticleInteraction.created_at)).offset(offset).limit(per_page).all()
    
    def is_article_saved(self, user_id: int, article_id: int):
        """Перевіряє, чи збережена стаття"""
        saved = self.db_session.query(ArticleInteraction).filter(
            and_(
                ArticleInteraction.user_id == user_id,
                ArticleInteraction.article_id == article_id,
                ArticleInteraction.interaction_type == 'saved',
                ArticleInteraction.value == 1
            )
        ).first()
        
        return saved is not None
