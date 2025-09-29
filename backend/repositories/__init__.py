from flask import g
from database import IDatabaseConnection


def get_admin_repo():
    """Повертає екземпляр UserRepository"""
    db_conn: IDatabaseConnection = g.container.resolve(IDatabaseConnection)
    session = db_conn.get_session()
    from repositories.user import UserRepository

    return UserRepository(session)


def get_subscription_repo():
    """Повертає екземпляр SubscriptionRepository"""
    db_conn: IDatabaseConnection = g.container.resolve(IDatabaseConnection)
    session = db_conn.get_session()
    from repositories.subscription import SubscriptionRepository

    return SubscriptionRepository(session)


def get_article_repo():
    """Повертає екземпляр ArticleRepository"""
    db_conn: IDatabaseConnection = g.container.resolve(IDatabaseConnection)
    session = db_conn.get_session()
    from repositories.article import ArticleRepository

    return ArticleRepository(session)


def get_admin_repo():
    """Повертає екземпляр AdminRepository"""
    db_conn: IDatabaseConnection = g.container.resolve(IDatabaseConnection)
    session = db_conn.get_session()
    from repositories.admin import AdminRepository

    return AdminRepository(session)


def get_category_repo():
    """Повертає екземпляр CategoryRepository"""
    db_conn: IDatabaseConnection = g.container.resolve(IDatabaseConnection)
    session = db_conn.get_session()
    from repositories.category import CategoryRepository

    return CategoryRepository(session)


def get_author_repo():
    """Повертає екземпляр AuthorRepository"""
    db_conn: IDatabaseConnection = g.container.resolve(IDatabaseConnection)
    session = db_conn.get_session()
    from repositories.author import AuthorRepository

    return AuthorRepository(session)


def get_ad_repo():
    """Повертає екземпляр AdRepository"""
    db_conn: IDatabaseConnection = g.container.resolve(IDatabaseConnection)
    session = db_conn.get_session()
    from repositories.ad import AdRepository

    return AdRepository(session)
