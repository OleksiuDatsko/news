# backend/models/ad.py
from sqlalchemy import Column, Text, BigInteger, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from models.base import BaseModel


class Ad(BaseModel):
    __tablename__ = "ads"

    title = Column(Text, nullable=False)
    content = Column(Text)
    ad_type = Column(Text, nullable=False, default="banner")
    is_active = Column(Boolean, nullable=False, default=True)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    impressions_count = Column(BigInteger, nullable=False, default=0)
    clicks_count = Column(BigInteger, nullable=False, default=0)

    ad_views = relationship("AdView", back_populates="ad")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "ad_type": self.ad_type,
            "is_active": self.is_active,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "impressions_count": self.impressions_count,
            "clicks_count": self.clicks_count,
        }


class AdView(BaseModel):
    __tablename__ = "ad_views"

    ad_id = Column(BigInteger, ForeignKey("ads.id"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    session_id = Column(Text)
    ip_address = Column(Text)
    viewed_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    # Relationships
    ad = relationship("Ad", back_populates="ad_views")
    user = relationship("User", back_populates="ad_views")

    def to_dict(self):
        return {
            "id": self.id,
            "ad_id": self.ad_id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "ip_address": self.ip_address,
            "viewed_at": self.viewed_at.isoformat(),
        }
