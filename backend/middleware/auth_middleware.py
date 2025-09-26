from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from repositories.user import get_user_repo
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
