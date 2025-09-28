from repositories.repositories import BaseRepository
from models.user import User
from sqlalchemy.orm import Session


class UserRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(db_session, User)

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
