from sqlalchemy.orm import Session
from repositories.interfaces import IUserRepository, IArticleRepository
from models.user import User
from models.article import Article

class UserRepository(IUserRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def create(self, user_data: dict):
        user = User(**user_data)
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user
    
    def get_by_id(self, user_id: int):
        return self.db_session.query(User).filter_by(id=user_id).first()
    
    def get_by_email(self, email: str):
        return self.db_session.query(User).filter_by(email=email).first()

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
