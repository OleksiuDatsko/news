from sqlalchemy.orm import Session
from sqlalchemy import desc, update
from .repositories import BaseRepository
from models.notification import Notification


class NotificationRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(db_session, Notification)

    def get_unread_by_user(self, user_id: int, limit: int = 10):
        """Отримує останні N непрочитаних сповіщень для користувача."""
        return (
            self.db_session.query(self.model)
            .filter_by(user_id=user_id, is_read=False)
            .order_by(desc(self.model.created_at))
            .limit(limit)
            .all()
        )

    def get_all_by_user(self, user_id: int, page: int = 1, per_page: int = 10):
        """Отримує всі сповіщення для користувача з пагінацією."""
        query = (
            self.db_session.query(self.model)
            .filter_by(user_id=user_id)
            .order_by(desc(self.model.created_at))
        )

        total = query.count()

        offset = (page - 1) * per_page
        notifications = query.offset(offset).limit(per_page).all()

        return notifications, total

    def mark_as_read(self, notification_id: int, user_id: int):
        """Позначає одне сповіщення як прочитане."""
        notification = self.get_by(id=notification_id, user_id=user_id)
        if notification and not notification.is_read:
            return self.update(notification, {"is_read": True})
        return notification

    def mark_all_as_read(self, user_id: int):
        """Позначає всі сповіщення користувача як прочитані."""
        self.db_session.query(self.model).filter_by(
            user_id=user_id, is_read=False
        ).update({"is_read": True})

        self.db_session.commit()
        return True
