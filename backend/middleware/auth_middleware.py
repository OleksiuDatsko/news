from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from functools import wraps
from repositories import get_user_repo, get_user_repo
from services.auth.admin import AdminAuthService
from services.auth.user import UserAuthService


def token_required(f):
    """Декоратор для перевірки JWT токену"""

    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        current_user_id = get_jwt_identity()
        current_user = UserAuthService(get_user_repo()).get_current_user(
            current_user_id
        )
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
                current_user = UserAuthService(get_user_repo()).get_current_user(
                    current_user_id
                )
                return f(current_user, *args, **kwargs)
        except:
            pass

        return f(None, *args, **kwargs)

    return decorated


def admin_token_required(f):
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        try:
            jwt = get_jwt()
            if jwt.get("type") != "admin":
                return jsonify({"msg": "Недостатньо прав"}), 403
            current_admin_id = get_jwt_identity()
            if current_admin_id:
                current_admin = AdminAuthService(get_user_repo()).get_current_admin(
                    current_admin_id
                )
                return f(current_admin, *args, **kwargs)
        except:
            pass

        return f(None, *args, **kwargs)

    return decorated
