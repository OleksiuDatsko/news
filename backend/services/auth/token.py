from datetime import timedelta
from flask_jwt_extended import create_access_token, create_refresh_token
import os
from typing import Dict, Any
from . import TokenFactory
from models.user import User
from models.admin import Admin


class UserTokenFactory(TokenFactory):
    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")
        self.algorithm = "HS256"
        self.default_expiration = 24 * 3600  # 24 години
        self.refresh_expiration = 7 * 24 * 3600  # 7 днів

    def create_token(self, user: User, **kwargs) -> Dict[str, Any]:
        expires_in: int = kwargs.get("expires_in", self.default_expiration)
        refresh_token_expires_in: int = kwargs.get(
            "refresh_token_expires_in", self.refresh_expiration
        )
        additional_claims: Dict[str, Any] = kwargs.get("additional_claims", {})

        additional_claims.update({"type": "user"})

        access_token = create_access_token(
            identity=str(user.id),
            expires_delta=timedelta(seconds=expires_in),
            additional_claims=additional_claims,
        )
        refresh_token = create_refresh_token(
            identity=str(user.id),
            expires_delta=timedelta(seconds=refresh_token_expires_in),
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "access_token_expires_in": expires_in,
            "refresh_token_expires_in": refresh_token_expires_in,
            "token_type": "Bearer",
        }

    def get_factory_type(self) -> str:
        return "user"


class AdminTokenFactory(TokenFactory):
    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")
        self.algorithm = "HS256"
        self.default_expiration = 3600  # 1 година
        self.refresh_expiration = 24 * 3600  # 24 години

    def create_token(self, user: User, **kwargs) -> Dict[str, Any]:
        expires_in: int = kwargs.get("expires_in", self.default_expiration)
        refresh_token_expires_in: int = kwargs.get(
            "refresh_token_expires_in", self.refresh_expiration
        )
        additional_claims: Dict[str, Any] = kwargs.get("additional_claims", {})

        additional_claims.update({"type": "admin"})

        access_token = create_access_token(
            identity=str(user.id),
            expires_delta=timedelta(seconds=expires_in),
            additional_claims=additional_claims,
        )
        refresh_token = create_refresh_token(
            identity=str(user.id),
            expires_delta=timedelta(seconds=refresh_token_expires_in),
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "access_token_expires_in": expires_in,
            "refresh_token_expires_in": refresh_token_expires_in,
            "token_type": "Bearer",
        }

    def get_factory_type(self) -> str:
        return "admin"


class TokenFactoryProducer:
    def __init__(self):
        self._factories = {
            "user": UserTokenFactory(),
            "admin": AdminTokenFactory(),
        }

    def get_factory(self, factory_type: str) -> TokenFactory:
        """Отримання factory за типом"""
        print(self._factories)
        if factory_type not in self._factories:
            raise ValueError(f"Невідомий тип factory: {factory_type}")

        return self._factories[factory_type]

    def create_tokens_for_user(
        self,
        user: User,
    ) -> Dict[str, Any]:
        """Створення токенів для користувача"""
        user_factory = self.get_factory("user")
        return user_factory.create_token(user)

    def create_tokens_for_admin(
        self,
        admin: Admin,
    ) -> Dict[str, Any]:
        """Створення токенів для адміністратора"""
        admin_factory = self.get_factory("admin")
        return admin_factory.create_token(admin)

    def get_available_factories(self) -> list:
        """Список доступних factories"""
        return list(self._factories.keys())
