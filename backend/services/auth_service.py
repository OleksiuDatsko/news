# backend/services/auth_service.py

from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from repositories.interfaces import IUserRepository
from datetime import timedelta

class AuthService:
    def __init__(self, user_repo: IUserRepository, access_expires: int = 3600, refresh_expires: int = 86400):
        self.user_repo = user_repo
        self.access_expires = timedelta(seconds=access_expires)
        self.refresh_expires = timedelta(seconds=refresh_expires)

    def register(self, email: str, password: str, username: str) -> dict:
        """
        Реєструє нового користувача.
        Повертає словник з access_token та refresh_token.
        Викидає ValueError, якщо користувач з таким email вже існує.
        """
        # Перевірка, чи не існує вже користувач з таким email
        existing_user = self.user_repo.get_by_email(email)
        if existing_user:
            raise ValueError("Користувач з таким email вже існує")

        # Хешування паролю
        hashed_password = generate_password_hash(password)

        # Створення користувача
        user_data = {
            "email": email,
            "password": hashed_password,
            "username": username,
            "preferences": {}
        }
        
        user = self.user_repo.create(user_data)

        access_token = create_access_token(identity=str(user.id), expires_delta=self.access_expires)
        refresh_token = create_refresh_token(identity=str(user.id), expires_delta=self.refresh_expires)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
            }
        }

    def authenticate(self, email: str, password: str) -> dict:
        """Існуючий метод для аутентифікації"""
        user = self.user_repo.get_by(email=email)
        print(user)
        if not user or not check_password_hash(user.password, password):
            raise ValueError("Невірний email або пароль")

        access_token = create_access_token(identity=str(user.id), expires_delta=self.access_expires)
        refresh_token = create_refresh_token(identity=str(user.id), expires_delta=self.refresh_expires)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
            }
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
        if not identity:
            raise ValueError("Не вдалося отримати дані користувача з токена")

        new_access = create_access_token(identity=identity, expires_delta=self.access_expires)
        return {"access_token": new_access}
    
    def get_current_user(self, user_id: int):
        """Повертає користувача за його ID"""
        user = self.user_repo.get_by(id=user_id)
        if not user:
            raise ValueError("Користувача не знайдено")
        return user
