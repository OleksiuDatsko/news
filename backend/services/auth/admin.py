from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import decode_token
from repositories.admin import AdminRepository
from . import AuthStrategy
from .token import TokenFactoryProducer


class AdminAuthService(AuthStrategy):
    def __init__(
        self,
        admin_repo: AdminRepository,
    ):
        self.admin_repo = admin_repo

    def register(self, email: str, password: str) -> dict:
        """
        Реєструє нового користувача.
        Повертає словник з access_token та refresh_token.
        Викидає ValueError, якщо користувач з таким email вже існує.
        """
        existing_user = self.admin_repo.get_by(email=email)
        if existing_user:
            raise ValueError("Адмін з таким email вже існує")

        hashed_password = generate_password_hash(password)

        data = {
            "email": email,
            "password": hashed_password,
        }

        admin = self.admin_repo.create(data)

        token_producer = TokenFactoryProducer()
        tokens = token_producer.create_tokens_for_admin(admin)
        print(tokens)
        return {
            "tokens": tokens,
            "admin": {
                "id": admin.id,
                "email": admin.email,
            },
        }

    def authenticate(self, email: str, password: str) -> dict:
        """Існуючий метод для аутентифікації"""
        admin = self.admin_repo.get_by(email=email)
        if not admin or not check_password_hash(admin.password, password):
            raise ValueError("Невірний email або пароль")

        token_producer = TokenFactoryProducer()
        tokens = token_producer.create_tokens_for_admin(admin)
        return {
            "tokens": tokens,
            "admin": admin.to_dict(),
        }

    def refresh(self, user: str) -> dict:
        """Існуючий метод для оновлення токена"""
        token_producer = TokenFactoryProducer()
        tokens = token_producer.create_tokens_for_admin(user)
        return {"tokens": tokens}

    def get_current_admin(self, admin_id: int):
        """Повертає користувача за його ID"""
        admin = self.admin_repo.get_by(id=admin_id)
        if not admin:
            raise ValueError("Користувача не знайдено")
        return admin
