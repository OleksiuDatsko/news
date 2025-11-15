from flask import g
from repositories.repositories import BaseRepository
from models.admin import Admin
from sqlalchemy.orm import Session
from sqlalchemy import asc

class AdminRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(db_session, Admin)

    def get_paginated_admins(self, page: int, per_page: int):
        """
        Отримує пагінований список адміністраторів, сортованих за email.
        """
        return self.get_all_paginated(
            page=page,
            per_page=per_page,
            order_by_col="email",
            order_desc=False
        )