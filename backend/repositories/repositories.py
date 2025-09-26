from sqlalchemy import column
from sqlalchemy.orm import Session, query
from repositories.interfaces import IArticleRepository
from models.user import User
from models.article import Article

class BaseRepository:
    def __init__(self, db_session: Session, model):
        self.db_session = db_session
        self.model = model
    
    def get_by(self, **kwargs):
        return self.db_session.query(self.model).filter_by(**kwargs).first()
    
    def get_all(self):
        return self.db_session.query(self.model).all()
    
    def get_all_by(self, **kwargs):
        return self.db_session.query(self.model).filter_by(**kwargs).all()
    
    def create(self, data: dict):
        instace = self.model(**data)
        self.db_session.add(instace)
        self.db_session.commit()
        self.db_session.refresh(instace)
        return instace

class ArticleRepository(IArticleRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def create(self, article_data: dict):
        article = Article(**article_data)
        self.db_session.add(article)
        self.db_session.commit()
        self.db_session.refresh(article)
        return article
    
    def get_by_id(self, article_id: int):
        return self.db_session.query(Article).filter_by(id=article_id).first()
    
    def get_all(self, page: int = 1, per_page: int = 10, filters: dict = None):
        query = self.db_session.query(Article)
        
        if filters:
            if filters.get('status'):
                query = query.filter_by(status=filters['status'])
        
        offset = (page - 1) * per_page
        return query.offset(offset).limit(per_page).all()
