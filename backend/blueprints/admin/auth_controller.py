from flask import Blueprint, make_response, request, jsonify
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
)
from middleware.auth_middleware import admin_token_required
from repositories import get_admin_repo
from services.auth.admin import AdminAuthService as AuthService

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
@admin_token_required
def register(current_admin):
    data = request.get_json()

    if not data.get("email"):
        return jsonify({"msg": "Email є обов'язковим"}), 400
    if not data.get("password"):
        return jsonify({"msg": "Пароль є обов'язковим"}), 400

    admin_repo = get_admin_repo()
    auth_service = AuthService(admin_repo)

    try:
        result = auth_service.register(
            email=data.get("email"),
            password=data.get("password"),
        )
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    admin_repo = get_admin_repo()
    auth_service = AuthService(admin_repo)

    try:
        result = auth_service.authenticate(data.get("email"), data.get("password"))
        response = make_response(jsonify({"admin": result["admin"]}))

        set_access_cookies(response, result["tokens"]["access_token"])
        set_refresh_cookies(response, result["tokens"]["refresh_token"])

        return response, 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 401


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_admin_id = get_jwt_identity()
    admin_repo = get_admin_repo()
    auth_service = AuthService(admin_repo)
    admin = auth_service.get_current_admin(current_admin_id)

    new_tokens = auth_service.refresh(admin)

    response = make_response(jsonify({"msg": "Токен успішно оновлено"}))

    set_access_cookies(response, new_tokens["tokens"]["access_token"])

    return response, 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    response = make_response(jsonify({"msg": "Успішний вихід"}))
    unset_jwt_cookies(response)
    return response, 200


@auth_bp.route("/me", methods=["GET"])
@admin_token_required
def protected(current_admin):
    return (
        jsonify({"msg": "JWT працює корректно", "admin": current_admin.to_dict()}),
        200,
    )
