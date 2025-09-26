from flask import g
from sqlalchemy.orm import Session
from repositories.repositories import BaseRepository
from database import IDatabaseConnection
from models.subscription import SubscriptionPlan, UserSubscriptionPlan

class SubscriptionRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(db_session, SubscriptionPlan)

    def get_all_plans(self):
        return self.get_all()

    def get_plan_by_id(self, plan_id: int):
        return self.get_by(id=plan_id)

    def get_active_user_subscription(self, user_id: int):
        return (
            self.db_session.query(UserSubscriptionPlan)
            .filter_by(user_id=user_id, is_active=True)
            .order_by(UserSubscriptionPlan.start_date.desc())
            .first()
        )

    def subscribe_user(self, user_id: int, plan_id: int):
        prev = self.get_active_user_subscription(user_id)
        if prev:
            prev.is_active = False
            self.db_session.add(prev)

        new_sub = UserSubscriptionPlan(user_id=user_id, plan_id=plan_id, is_active=True)
        self.db_session.add(new_sub)
        self.db_session.commit()
        self.db_session.refresh(new_sub)
        return new_sub

    def get_user_subscription_history(self, user_id: int):
        return (
            self.db_session.query(UserSubscriptionPlan)
            .filter_by(user_id=user_id)
            .order_by(UserSubscriptionPlan.start_date.desc())
            .all()
        )
