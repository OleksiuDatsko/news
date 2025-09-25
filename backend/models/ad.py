from sqlalchemy import Column, Text, Boolean, BigInteger, DateTime, ForeignKey, Numeric, func
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

    views = relationship("AdView", back_populates="ad")

class AdView(BaseModel):
    __tablename__ = "ad_views"
    ad_id = Column(BigInteger, ForeignKey("ads.id"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    session_id = Column(Text)
    ip_address = Column(Text)
    viewed_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    ad = relationship("Ad", back_populates="views")
    user = relationship("User", back_populates="ad_views")
