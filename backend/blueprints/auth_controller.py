from flask import Blueprint, request, jsonify
from middleware.auth_middleware import token_required
from repositories import get_admin_repo
from services.auth.user import UserAuthService as AuthService

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data.get("email"):
        return jsonify({"msg": "Email є обов'язковим"}), 400
    if not data.get("password"):
        return jsonify({"msg": "Пароль є обов'язковим"}), 400
    if not data.get("username"):
        return jsonify({"msg": "Ім'я користувача є обов'язковим"}), 400

    user_repo = get_admin_repo()
    auth_service = AuthService(user_repo)

    try:
        result = auth_service.register(
            email=data.get("email"),
            password=data.get("password"),
            username=data.get("username"),
        )
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user_repo = get_admin_repo()
    auth_service = AuthService(user_repo)

    try:
        result = auth_service.authenticate(data.get("email"), data.get("password"))
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 401


@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    data = request.get_json()
    user_repo = get_admin_repo()
    auth_service = AuthService(user_repo)

    try:
        result = auth_service.refresh(data.get("refresh_token"))
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 401


@auth_bp.route("/me", methods=["GET"])
@token_required
def protected(current_user):
    return jsonify({"msg": "JWT працює корректно", "user": current_user.to_dict()}), 200
