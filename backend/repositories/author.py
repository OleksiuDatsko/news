from repositories.repositories import BaseRepository
from models.author import Author
from sqlalchemy.orm import Session
from sqlalchemy import asc, or_


class AuthorRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(db_session, Author)

    def get_paginated_authors(self, page: int, per_page: int, search_query: str | None):
        """
        Отримує пагінований список авторів з пошуком.
        """
        query = self.db_session.query(self.model)

        if search_query:
            search_term = f"%{search_query.lower()}%"
            query = query.filter(
                or_(
                    self.model.first_name.ilike(search_term),
                    self.model.last_name.ilike(search_term),
                    self.model.bio.ilike(search_term),
                )
            )

        total = query.count()
        offset = (page - 1) * per_page

        authors = (
            query.order_by(asc(self.model.last_name))
            .offset(offset)
            .limit(per_page)
            .all()
        )

        return authors, total
