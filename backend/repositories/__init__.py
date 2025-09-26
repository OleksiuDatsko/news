from flask import g
from database import IDatabaseConnection
from repositories.subscription import SubscriptionRepository
from repositories.user import UserRepository


def get_user_repo():
    """
    Повертає екземпляр UserRepository, використовуючи контейнер із flask.g.
    """
    db_conn: IDatabaseConnection = g.container.resolve(IDatabaseConnection)
    session = db_conn.get_session()
    return UserRepository(session)


def get_subscription_repo():
    """
    Повертає екземпляр SubscriptionRepository, використовуючи контейнер із flask.g.
    """
    db_conn: IDatabaseConnection = g.container.resolve(IDatabaseConnection)
    session = db_conn.get_session()
    return SubscriptionRepository(session)
