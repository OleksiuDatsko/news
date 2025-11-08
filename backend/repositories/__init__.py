from flask import g
from .article_view import ArticleViewRepository
from .notification import NotificationRepository
from .ad import AdRepository
from .ad_view import AdViewRepository
from .admin import AdminRepository
from .article import ArticleRepository
from .author import AuthorRepository
from .category import CategoryRepository
from .comment import CommentRepository
from .subscription import SubscriptionRepository
from .user import UserRepository

def get_ad_repo() -> AdRepository:
    return AdRepository(g.db_session)

def get_ad_view_repo() -> AdViewRepository:
    return AdViewRepository(g.db_session)

def get_admin_repo() -> AdminRepository:
    return AdminRepository(g.db_session)

def get_article_repo() -> ArticleRepository:
    return ArticleRepository(g.db_session)

def get_author_repo() -> AuthorRepository:
    return AuthorRepository(g.db_session)

def get_category_repo() -> CategoryRepository:
    return CategoryRepository(g.db_session)

def get_comment_repo() -> CommentRepository:
    return CommentRepository(g.db_session)

def get_subscription_repo() -> SubscriptionRepository:
    return SubscriptionRepository(g.db_session)

def get_user_repo() -> UserRepository:
    return UserRepository(g.db_session)

def get_notification_repo() -> NotificationRepository:
    return NotificationRepository(g.db_session)

def get_article_view_repo() -> ArticleViewRepository:
    return ArticleViewRepository(g.db_session)