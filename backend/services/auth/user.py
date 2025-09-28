from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import decode_token
from repositories.interfaces import IUserRepository
from datetime import timedelta
from . import AuthStrategy
from .token import TokenFactoryProducer


class UserAuthService(AuthStrategy):
    def __init__(
        self,
        user_repo: IUserRepository,
    ):
        self.user_repo = user_repo

    def register(self, email: str, password: str, username: str) -> dict:
        """
        Реєструє нового користувача.
        Повертає словник з access_token та refresh_token.
        Викидає ValueError, якщо користувач з таким email вже існує.
        """
        existing_user = self.user_repo.get_by(email=email) or self.user_repo.get_by(
            username=username
        )
        if existing_user:
            raise ValueError("Користувач з таким email або ім'ям вже існує")

        hashed_password = generate_password_hash(password)

        user_data = {
            "email": email,
            "password": hashed_password,
            "username": username,
            "preferences": {},
        }

        user = self.user_repo.create(user_data)

        token_producer = TokenFactoryProducer()
        tokens = token_producer.create_tokens_for_user(user)
        print(tokens)
        return {
            "tokens": tokens,
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
            },
        }

    def authenticate(self, email: str, password: str) -> dict:
        """Існуючий метод для аутентифікації"""
        user = self.user_repo.get_by(email=email)
        if not user or not check_password_hash(user.password, password):
            raise ValueError("Невірний email або пароль")

        token_producer = TokenFactoryProducer()
        tokens = token_producer.create_tokens_for_user(user)
        return {
            "tokens": tokens,
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
            },
        }

    def refresh(self, refresh_token: str) -> dict:
        """Існуючий метод для оновлення токена"""
        try:
            decoded = decode_token(refresh_token)
        except Exception as e:
            raise ValueError("Невірний refresh token") from e

        if decoded.get("type") != "refresh":
            raise ValueError("Переданий не refresh token")

        identity = decoded.get("sub")
        user = self.user_repo.get_by(id=identity)
        if not identity:
            raise ValueError("Не вдалося отримати дані користувача з токена")

        token_producer = TokenFactoryProducer()
        tokens = token_producer.create_tokens_for_user(user)

        return {"tokens": tokens}

    def get_current_user(self, user_id: int):
        """Повертає користувача за його ID"""
        user = self.user_repo.get_by(id=user_id)
        if not user:
            raise ValueError("Користувача не знайдено")
        return user
