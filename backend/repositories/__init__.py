from flask import g
from database import IDatabaseConnection
from repositories.subscription import SubscriptionRepository
from repositories.user import UserRepository
from repositories.article import ArticleRepository


def get_user_repo():
    """Повертає екземпляр UserRepository"""
    db_conn: IDatabaseConnection = g.container.resolve(IDatabaseConnection)
    session = db_conn.get_session()
    return UserRepository(session)


def get_subscription_repo():
    """Повертає екземпляр SubscriptionRepository"""
    db_conn: IDatabaseConnection = g.container.resolve(IDatabaseConnection)
    session = db_conn.get_session()
    return SubscriptionRepository(session)


def get_article_repo():
    """Повертає екземпляр ArticleRepository"""
    db_conn: IDatabaseConnection = g.container.resolve(IDatabaseConnection)
    session = db_conn.get_session()
    return ArticleRepository(session)

def get_admin_repo():
    """Повертає екземпляр AdminRepository"""
    db_conn: IDatabaseConnection = g.container.resolve(IDatabaseConnection)
    session = db_conn.get_session()
    from repositories.admin import AdminRepository
    return AdminRepository(session)