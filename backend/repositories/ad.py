import datetime

from sqlalchemy import desc
from repositories.repositories import BaseRepository
from models.ad import Ad
from sqlalchemy.orm import Session


class AdRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(db_session, Ad)

    def get_paginated_ads(
        self, page: int, per_page: int, status: str | None, ad_type: str | None
    ):
        """
        Отримує пагінований список рекламних оголошень з фільтрами.
        """
        query = self.db_session.query(self.model)
        current_time = datetime.now()

        if status == "active":
            query = query.filter(
                self.model.is_active == True,
                (self.model.end_date == None) | (self.model.end_date > current_time),
            )
        elif status == "inactive":
            query = query.filter(self.model.is_active == False)
        elif status == "expired":
            query = query.filter(
                (self.model.end_date != None) & (self.model.end_date < current_time)
            )

        if ad_type:
            query = query.filter(self.model.ad_type == ad_type)

        total = query.count()

        offset = (page - 1) * per_page
        ads = query.order_by(desc(self.model.id)).offset(offset).limit(per_page).all()

        return ads, total
