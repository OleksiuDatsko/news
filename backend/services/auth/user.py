from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import decode_token
from repositories.user import UserRepository
from . import AuthStrategy
from .token import TokenFactoryProducer


class UserAuthService(AuthStrategy):
    def __init__(
        self,
        user_repo: UserRepository,
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
            "user": user.to_dict(),
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
            "user": user.to_dict(),
        }

    def refresh(self, user: str) -> dict:
        """Існуючий метод для оновлення токена"""
        token_producer = TokenFactoryProducer()
        tokens = token_producer.create_tokens_for_user(user)
        return {"tokens": tokens}

    def get_current_user(self, user_id: int):
        """Повертає користувача за його ID"""
        user = self.user_repo.get_by(id=user_id)
        if not user:
            raise ValueError("Користувача не знайдено")
        return user
