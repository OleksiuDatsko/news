from repositories.repositories import BaseRepository
from models.user import User
from sqlalchemy.orm import Session
from sqlalchemy import asc

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

    def get_paginated_users(self, page: int, per_page: int):
        """
        Отримує пагінований список користувачів, сортованих за username.
        """
        return self.get_all_paginated(
            page=page,
            per_page=per_page,
            order_by_col="username",
            order_desc=False
        )
