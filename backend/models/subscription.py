from sqlalchemy import (
    Column,
    Text,
    JSON,
    BigInteger,
    DateTime,
    ForeignKey,
    Boolean,
    Numeric,
    func,
)
from sqlalchemy.orm import relationship
from models.base import BaseModel


class SubscriptionPlan(BaseModel):
    __tablename__ = "subscription_plans"
    name = Column(Text, nullable=False)
    permissions = Column(JSON, nullable=False)
    price_per_month = Column(Numeric)
    description = Column(Text)

    users = relationship("UserSubscriptionPlan", back_populates="plan")


class UserSubscriptionPlan(BaseModel):
    __tablename__ = "user_subscription_plans"
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    plan_id = Column(BigInteger, ForeignKey("subscription_plans.id"), nullable=False)
    start_date = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, nullable=False, default=True)

    user = relationship("User", back_populates="subscriptions")
    plan = relationship("SubscriptionPlan", back_populates="users")

    @property
    def left_days(self):
        if self.plan.price_per_month is None:
            return None
        from datetime import datetime, timedelta

        elapsed = timedelta(days=(datetime.now() - self.start_date).days).days
        return max(0, 30 - elapsed)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "plan_id": self.plan_id,
            "start_date": self.start_date.isoformat(),
            "is_active": self.is_active,
            "plan": {
                "name": self.plan.name,
                "permissions": self.plan.permissions,
                "price_per_month": (
                    float(self.plan.price_per_month)
                    if self.plan.price_per_month
                    else None
                ),
                "description": self.plan.description,
            },
            "left_days": self.left_days,
        }
