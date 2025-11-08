from abc import ABC, abstractmethod
import json
import os
from typing import List
from sqlalchemy.orm import Session
from pywebpush import WebPusher, WebPushException, webpush
from models.push_subscription import PushSubscription
from models.article import Article
from models.user import User
from models.notification import Notification

VAPID_PUBLIC_KEY = os.environ.get("VAPID_PUBLIC_KEY")
VAPID_PRIVATE_KEY = os.environ.get("VAPID_PRIVATE_KEY")
VAPID_CLAIMS = {"sub": os.environ.get("VAPID_ADMIN_EMAIL")}


def send_web_push(subscription_info, message_body):
    try:
        webpush(
            subscription_info={
                "endpoint": subscription_info.endpoint,
                "keys": {
                    "p256dh": subscription_info.p256dh,
                    "auth": subscription_info.auth,
                },
            },
            data=json.dumps(message_body),
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims=VAPID_CLAIMS,
        )
        return True
    except WebPushException as e:
        print(f"Push failed: {e}")
        return False


class AbstractArticleObserver(ABC):
    @abstractmethod
    def update(self, article: Article, db_session: Session):
        pass


class BreakingNewsNotifier(AbstractArticleObserver):
    def update(self, article: Article, db_session: Session):
        if not article.is_breaking:
            return

        print(
            f"[Observer] BreakingNewsNotifier: Стаття {article.id} термінова. Шукаю підписників..."
        )
        users_to_notify = (
            db_session.query(User)
            .filter(User.preferences["breakingNews"].as_boolean() == True)
            .all()
        )

        notifications = []
        for user in users_to_notify:
            notifications.append(
                Notification(
                    user_id=user.id,
                    article_id=article.id,
                    type="breaking_news",
                    title=f"ТЕРМІНОВО: {article.title}",
                    message=f"Щойно опублікована термінова новина.",
                )
            )

        if notifications:
            db_session.add_all(notifications)
            print(
                f"[Observer] BreakingNewsNotifier: Створено {len(notifications)} сповіщень."
            )


class CategoryNotifier(AbstractArticleObserver):
    def update(self, article: Article, db_session: Session):
        if not article.category or not article.category.slug:
            return

        category_slug = article.category.slug
        print(
            f"[Observer] CategoryNotifier: Стаття {article.id} в рубриці '{category_slug}'. Шукаю підписників..."
        )

        users_to_notify = (
            db_session.query(User)
            .filter(User.preferences["favorite_categories"].contains(category_slug))
            .all()
        )

        notifications = []
        for user in users_to_notify:
            notifications.append(
                Notification(
                    user_id=user.id,
                    article_id=article.id,
                    type="favorite_category",
                    title=f"Нове в рубриці «{article.category.name}»",
                    message=f"Опубліковано нову статтю: {article.title}",
                )
            )

        if notifications:
            db_session.add_all(notifications)
            print(
                f"[Observer] CategoryNotifier: Створено {len(notifications)} сповіщень."
            )


class AuthorNotifier(AbstractArticleObserver):
    def update(self, article: Article, db_session: Session):
        """
        Сповіщає користувачів, які підписані на автора цієї статті.
        Використовує ефективний M2M-зв'язок 'author.followers'.
        """
        if not article.author:
            print(f"[Observer] AuthorNotifier: У статті {article.id} відсутній автор.")
            return

        author = article.author
        print(
            f"[Observer] AuthorNotifier: Стаття {article.id} від автора {author.id}. Шукаю підписників..."
        )

        users_to_notify = author.followers.all()

        if not users_to_notify:
            print(
                f"[Observer] AuthorNotifier: 0 підписників знайдено для автора {author.id}."
            )
            return

        notifications = []
        author_name = f"{author.first_name} {author.last_name}"
        push_payload = {
            "title": f"Нова стаття від {author_name}",
            "body": f"«{article.title}»",
            "url": f"/articles/{article.id}",
        }
        user_ids_to_notify = []

        for user in users_to_notify:
            notifications.append(
                Notification(
                    user_id=user.id,
                    article_id=article.id,
                    type="new_article_author",
                    title=push_payload["title"],
                    message=push_payload["body"],
                )
            )
            user_ids_to_notify.append(user.id)

        if notifications:
            db_session.add_all(notifications)
            print(
                f"[Observer] AuthorNotifier: Створено {len(notifications)} сповіщень."
            )
        subscriptions = (
            db_session.query(PushSubscription)
            .filter(PushSubscription.user_id.in_(user_ids_to_notify))
            .all()
        )

        print(f"[WebPush] Знайдено {len(subscriptions)} підписок для відправки.")
        for sub in subscriptions:
            send_web_push(sub, push_payload)


class ArticleNotificationService:
    """
    Це наш Суб'єкт. Він керує списком спостерігачів і
    сповіщає їх про публікацію статті.
    """

    def __init__(self):
        self._observers: List[AbstractArticleObserver] = []

    def attach(self, observer: AbstractArticleObserver):
        if observer not in self._observers:
            self._observers.append(observer)
            print(
                f"[Subject] Зареєстровано спостерігача: {observer.__class__.__name__}"
            )

    def detach(self, observer: AbstractArticleObserver):
        self._observers.remove(observer)

    def notify(self, article: Article, db_session: Session):
        """
        Сповістити всіх підписаних спостерігачів про нову статтю.
        """
        print(
            f"[Subject] Сповіщаю {len(self._observers)} спостерігачів про статтю {article.id}..."
        )
        for observer in self._observers:
            try:
                observer.update(article, db_session)
            except Exception as e:
                print(f"[Subject] ПОМИЛКА в {observer.__class__.__name__}: {e}")


notification_service = ArticleNotificationService()

notification_service.attach(BreakingNewsNotifier())
notification_service.attach(CategoryNotifier())
notification_service.attach(AuthorNotifier())

print("Сервіс сповіщень ініціалізовано.")
