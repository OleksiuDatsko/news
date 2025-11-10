from datetime import datetime
from repositories import get_article_view_repo
from repositories.article import ArticleRepository
from typing import List, Dict, Optional


class ArticleService:
    def __init__(self, article_repo: ArticleRepository):
        self.article_repo = article_repo

    def get_articles(
        self, page: int = 1, per_page: int = 10, filters: dict = None
    ) -> List:
        """Отримує список статей з фільтрами"""
        return self.article_repo.get_all(page=page, per_page=per_page, filters=filters)

    def search_articles(
        self,
        query: str,
        page: int = 1,
        per_page: int = 10,
        user_permissions: dict = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ):
        """
        Сервісний шар для пошуку статей.
        """
        if not query or len(query) < 3:
            return [], 0

        return self.article_repo.search(
            query,
            page,
            per_page,
            user_permissions=user_permissions,
            date_from=date_from,
            date_to=date_to,
        )

    def get_article_by_id(self, article_id: int, user_id: Optional[int] = None) -> Dict:
        """Отримує статтю за ID з додатковою інформацією"""
        article = self.article_repo.get_by_id(article_id)
        if not article:
            raise ValueError("Статтю не знайдено")

        result = article.to_dict()

        if user_id:
            result["is_saved"] = self.article_repo.is_article_saved(user_id, article_id)
            result["is_liked"] = self.article_repo.is_article_liked(user_id, article_id)

        return result

    def save_article(self, user_id: int, article_id: int) -> Dict:
        """Зберігає статтю для користувача"""
        article = self.article_repo.get_by_id(article_id)
        if not article:
            raise ValueError("Статтю не знайдено")

        self.article_repo.save_article(user_id, article_id)
        return {"message": "Статтю збережено", "is_saved": True}

    def unsave_article(self, user_id: int, article_id: int) -> Dict:
        """Прибирає статтю зі збережених"""
        article = self.article_repo.get_by_id(article_id)
        if not article:
            raise ValueError("Статтю не знайдено")

        self.article_repo.unsave_article(user_id, article_id)
        return {"message": "Статтю прибрано зі збережених", "is_saved": False}

    def get_saved_articles(
        self, user_id: int, page: int = 1, per_page: int = 10
    ) -> List[Dict]:
        """Отримує збережені статті користувача"""
        articles = self.article_repo.get_saved_articles(user_id, page, per_page)
        result = []

        for article in articles:
            article_dict = article.to_dict(metadata=True)
            article_dict["is_saved"] = True
            result.append(article_dict)

        return result

    def get_liked_articles(
        self, user_id: int, page: int = 1, per_page: int = 10
    ) -> List[Dict]:
        """Отримує статті, які лайкнув користувач"""
        articles = self.article_repo.get_liked_articles(user_id, page, per_page)
        result = []

        for article in articles:
            article_dict = article.to_dict(metadata=True)
            article_dict["is_liked"] = True
            article_dict["is_saved"] = self.article_repo.is_article_saved(
                user_id, article.id
            )
            result.append(article_dict)

        return result

    def toggle_save_article(self, user_id: int, article_id: int) -> Dict:
        """Перемикає статус збереження статті"""
        is_saved = self.article_repo.is_article_saved(user_id, article_id)

        if is_saved:
            return self.unsave_article(user_id, article_id)
        else:
            return self.save_article(user_id, article_id)

    def toggle_like_article(self, user_id: int, article_id: int) -> Dict:
        """Перемикає статус лайка статті"""
        article = self.article_repo.get_by_id(article_id)
        if not article:
            raise ValueError("Статтю не знайдено")

        is_liked = self.article_repo.toggle_like_article(user_id, article_id)

        if is_liked:
            return {"message": "Статтю вподобано", "is_liked": True}
        else:
            return {"message": "Лайк знято", "is_liked": False}

    def get_recommended_articles(
        self,
        user_id: int,
        page: int = 1,
        per_page: int = 10,
        favorite_category_slugs: list[str] = None,
        filters: dict = None,
    ):
        """
        Сервісний шар для виклику репозиторію рекомендованих статей.
        """
        return self.article_repo.get_recommended(
            page=page,
            per_page=per_page,
            user_id=user_id,
            favorite_category_slugs=favorite_category_slugs,
            filters=filters,
        )

    def record_article_impression(
        self,
        article_id: int,
        user_id: Optional[int] = None,
        session_id: Optional[str] = None,
        ip_address: Optional[str] = None,
    ) -> bool:
        """
        Реєструє показ картки статті.
        1. Збільшує лічильник views_count у статті.
        2. Створює запис ArticleView.
        """
        article = self.article_repo.get_by(id=article_id)
        if not article:
            raise ValueError("Статтю не знайдено")

        self.article_repo.update(
            article, {"views_count": (article.views_count or 0) + 1}
        )

        article_view_repo = get_article_view_repo()
        article_view_repo.create(
            {
                "article_id": article_id,
                "user_id": user_id,
                "session_id": session_id,
                "ip_address": ip_address,
                "viewed_at": datetime.now(),
            }
        )
        return True
