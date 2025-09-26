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
        @token_required
        def decorated(current_user, *args, **kwargs):
            user_permissions = list()
            for sub in current_user.subscriptions:
                if sub.is_active:
                    user_permissions = sub.plan.permissions
            for permission in permissions:
              if not user_permissions.get(permission, False):
                  return jsonify({"msg": "Недостатньо прав для доступу до цього ресурсу"}), 403
            return f(current_user, *args, **kwargs)
        return decorated
    return decorator