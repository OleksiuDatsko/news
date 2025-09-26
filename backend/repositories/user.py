from flask import g
from database import IDatabaseConnection
from models.user import User
from repositories.interfaces import IUserRepository
from sqlalchemy.orm import Session


def get_user_repo():
    """
    Повертає екземпляр UserRepository, використовуючи контейнер із flask.g.
    """
    db_conn: IDatabaseConnection = g.container.resolve(IDatabaseConnection)
    session = db_conn.get_session()
    return UserRepository(session)

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
