from flask import g
from repositories.notification import NotificationRepository
from repositories.ad import AdRepository
from repositories.ad_view import AdViewRepository
from repositories.admin import AdminRepository
from repositories.article import ArticleRepository
from repositories.author import AuthorRepository
from repositories.category import CategoryRepository
from repositories.comment import CommentRepository
from repositories.subscription import SubscriptionRepository
from repositories.user import UserRepository

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