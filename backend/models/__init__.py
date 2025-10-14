from sqlalchemy.ext.declarative import declarative_base
from .ad import Ad, AdView
from .article import Article, ArticleInteraction, ArticleView, Comment
from .category import Category
from .newsletter import NewsletterSubscription
from .notification import Notification
from .author import Author
from .user import User
from .subscription import UserSubscriptionPlan, SubscriptionPlan
from .admin import Admin

Base = declarative_base()

__all__ = [
    "Base",
    "Ad",
    "AdView",
    "Article",
    "ArticleInteraction",
    "ArticleView",
    "Category",
    "NewsletterSubscription",
    "Notification",
    "Author",
    "User",
    "UserSubscriptionPlan",
    "SubscriptionPlan",
    "Comment",
    "Admin",
]
