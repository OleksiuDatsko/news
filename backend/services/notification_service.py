from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.orm import Session
from models.article import Article
from models.user import User
from models.notification import Notification

class AbstractArticleObserver(ABC):
    @abstractmethod
    def update(self, article: Article, db_session: Session):
        pass

class BreakingNewsNotifier(AbstractArticleObserver):
    def update(self, article: Article, db_session: Session):
        if not article.is_breaking:
            return

        print(f"[Observer] BreakingNewsNotifier: Стаття {article.id} термінова. Шукаю підписників...")
        users_to_notify = db_session.query(User).filter(
            User.preferences["breakingNews"].as_boolean() == True
        ).all()

        notifications = []
        for user in users_to_notify:
            notifications.append(
                Notification(
                    user_id=user.id,
                    article_id=article.id,
                    type="breaking_news",
                    title=f"ТЕРМІНОВО: {article.title}",
                    message=f"Щойно опублікована термінова новина."
                )
            )
        
        if notifications:
            db_session.add_all(notifications)
            print(f"[Observer] BreakingNewsNotifier: Створено {len(notifications)} сповіщень.")

class CategoryNotifier(AbstractArticleObserver):
    def update(self, article: Article, db_session: Session):
        if not article.category or not article.category.slug:
            return
        
        category_slug = article.category.slug
        print(f"[Observer] CategoryNotifier: Стаття {article.id} в рубриці '{category_slug}'. Шукаю підписників...")

        users_to_notify = db_session.query(User).filter(
            User.preferences["favorite_categories"].contains(category_slug)
        ).all()

        notifications = []
        for user in users_to_notify:
            notifications.append(
                Notification(
                    user_id=user.id,
                    article_id=article.id,
                    type="favorite_category",
                    title=f"Нове в рубриці «{article.category.name}»",
                    message=f"Опубліковано нову статтю: {article.title}"
                )
            )
            
        if notifications:
            db_session.add_all(notifications)
            print(f"[Observer] CategoryNotifier: Створено {len(notifications)} сповіщень.")

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
            print(f"[Subject] Зареєстровано спостерігача: {observer.__class__.__name__}")

    def detach(self, observer: AbstractArticleObserver):
        self._observers.remove(observer)

    def notify(self, article: Article, db_session: Session):
        """
        Сповістити всіх підписаних спостерігачів про нову статтю.
        """
        print(f"[Subject] Сповіщаю {len(self._observers)} спостерігачів про статтю {article.id}...")
        for observer in self._observers:
            try:
                observer.update(article, db_session)
            except Exception as e:
                print(f"[Subject] ПОМИЛКА в {observer.__class__.__name__}: {e}")

notification_service = ArticleNotificationService()

notification_service.attach(BreakingNewsNotifier())
notification_service.attach(CategoryNotifier())

print("Сервіс сповіщень ініціалізовано.")