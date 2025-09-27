from repositories.article import ArticleRepository
from typing import List, Dict, Optional


class ArticleService:
    def __init__(self, article_repo: ArticleRepository):
        self.article_repo = article_repo

    def get_articles(self, page: int = 1, per_page: int = 10, filters: dict = None) -> List:
        """Отримує список статей з фільтрами"""
        return self.article_repo.get_all(page=page, per_page=per_page, filters=filters)

    def get_article_by_id(self, article_id: int, user_id: Optional[int] = None) -> Dict:
        """Отримує статтю за ID з додатковою інформацією"""
        article = self.article_repo.get_by_id(article_id)
        if not article:
            raise ValueError("Статтю не знайдено")
        
        result = article.to_dict()
        
        if user_id:
            result['is_saved'] = self.article_repo.is_article_saved(user_id, article_id)
        
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

    def get_saved_articles(self, user_id: int, page: int = 1, per_page: int = 10) -> List[Dict]:
        """Отримує збережені статті користувача"""
        articles = self.article_repo.get_saved_articles(user_id, page, per_page)
        result = []
        
        for article in articles:
            article_dict = article.to_dict(metadata=True)
            article_dict['is_saved'] = True  # Всі статті в цьому списку збережені
            result.append(article_dict)
        
        return result

    def toggle_save_article(self, user_id: int, article_id: int) -> Dict:
        """Перемикає статус збереження статті"""
        is_saved = self.article_repo.is_article_saved(user_id, article_id)
        
        if is_saved:
            return self.unsave_article(user_id, article_id)
        else:
            return self.save_article(user_id, article_id)
