from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from repositories import get_user_repo
from services.auth_service import AuthService


def token_required(f):
    """Декоратор для перевірки JWT токену"""

    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        current_user_id = get_jwt_identity()
        current_user = AuthService(get_user_repo()).get_current_user(current_user_id)
        return f(current_user, *args, **kwargs)

    return decorated


def permission_required(*permissions):
    """Декоратор для перевірки наявності певного дозволу у користувача"""

    def decorator(f):
        @wraps(f)
        def decorated(current_user, *args, **kwargs):
            user_permissions = current_user.permissions
            print(user_permissions, permissions)
            for permission in permissions:
                print(permission, user_permissions.get(permission, False))
                if not user_permissions.get(permission, False):
                    return (
                        jsonify(
                            {"msg": "Недостатньо прав для доступу до цього ресурсу"}
                        ),
                        403,
                    )
            return f(current_user, *args, **kwargs)

        return decorated

    return decorator


def token_optional(f):
    """Декоратор, що дозволяє опціональну авторизацію"""
    @wraps(f)
    @jwt_required(optional=True)
    def decorated(*args, **kwargs):
        try:
            current_user_id = get_jwt_identity()
            if current_user_id:
                current_user = AuthService(get_user_repo()).get_current_user(
                    current_user_id
                )
                return f(current_user, *args, **kwargs)
        except:
            pass

        return f(None, *args, **kwargs)

    return decorated
