from repositories.comment import CommentRepository
from repositories.article import ArticleRepository
from typing import List, Dict

class CommentService:
    def __init__(self, comment_repo: CommentRepository, article_repo: ArticleRepository):
        self.comment_repo = comment_repo
        self.article_repo = article_repo
        
    def get_comment_by_id(self, comment_id: int) -> Dict:
        """Отримує коментар за ID"""
        comment = self.comment_repo.get_by(id=comment_id)
        if not comment:
            raise ValueError("Коментар не знайдено")
        return comment.to_dict()

    def get_comments_for_article(self, article_id: int, page: int = 1, per_page: int = 10) -> List[Dict]:
        """Отримує список коментарів для статті"""
        # Перевіряємо, чи існує стаття
        article = self.article_repo.get_by_id(article_id)
        if not article:
            raise ValueError("Статтю не знайдено")
            
        comments = self.comment_repo.get_by_article(article_id, page, per_page)
        # Використовуємо to_dict з моделі Comment, яка повертає і дані юзера
        return [comment.to_dict() for comment in comments]

    def create_comment(self, user_id: int, article_id: int, text: str) -> Dict:
        """Створює новий коментар"""
        article = self.article_repo.get_by_id(article_id)
        if not article:
            raise ValueError("Статтю не знайдено")

        if not text or len(text.strip()) == 0:
            raise ValueError("Текст коментаря не може бути порожнім")

        comment_data = {
            "user_id": user_id,
            "article_id": article_id,
            "text": text,
            "status": "active",
        }
        new_comment = self.comment_repo.create(comment_data)
        return new_comment.to_dict()

    def update_comment(self, user_id: int, comment_id: int, text: str) -> Dict:
        """Оновлює існуючий коментар, перевіряючи власника"""
        comment = self.comment_repo.get_by(id=comment_id)
        if not comment:
            raise ValueError("Коментар не знайдено")

        if comment.user_id != user_id:
            raise PermissionError("Ви не можете редагувати чужий коментар")

        if not text or len(text.strip()) == 0:
            raise ValueError("Текст коментаря не може бути порожнім")

        updated_comment = self.comment_repo.update(comment, {"text": text})
        return updated_comment.to_dict()

    def delete_comment(self, user_id: int, comment_id: int, is_admin: bool = False):
        """Видаляє коментар, перевіряючи власника або права адміністратора"""
        comment = self.comment_repo.get_by(id=comment_id)
        if not comment:
            raise ValueError("Коментар не знайдено")

        if not is_admin and comment.user_id != user_id:
            raise PermissionError("Ви не можете видалити чужий коментар")

        self.comment_repo.delete(comment)
        return {"message": "Коментар успішно видалено"}