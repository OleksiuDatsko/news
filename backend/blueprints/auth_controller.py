from flask import Blueprint, request, jsonify, make_response, render_template
from services.subscribtion_service import SubscriptionService
from repositories import get_subscription_repo, get_user_repo
from services.auth.user import UserAuthService as AuthService
from flask_jwt_extended import (
    get_jwt,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
    jwt_required,
    get_jwt_identity,
)

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

    user_repo = get_user_repo()
    auth_service = AuthService(user_repo)

    try:
        result = auth_service.register(
            email=data.get("email"),
            password=data.get("password"),
            username=data.get("username"),
        )

        response = make_response(jsonify({"user": result["user"]}))

        set_access_cookies(response, result["tokens"]["access_token"])
        set_refresh_cookies(response, result["tokens"]["refresh_token"])

        new_user_id = result["user"]["id"]
        try:
            sub_repo = get_subscription_repo()
            sub_service = SubscriptionService(sub_repo)
            free_plan = sub_repo.get_by(name="Безкоштовний")
            if free_plan:
                sub_service.subscribe(new_user_id, free_plan.id)
        except Exception as e:
            print(f"Warning: Не вдалося підписати {new_user_id} на Free план: {e}")

        return response, 201
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user_repo = get_user_repo()
    auth_service = AuthService(user_repo)

    try:
        result = auth_service.authenticate(data.get("email"), data.get("password"))

        response = make_response(jsonify({"user": result["user"]}))

        set_access_cookies(response, result["tokens"]["access_token"])
        set_refresh_cookies(response, result["tokens"]["refresh_token"])

        return response, 200

    except ValueError as e:
        return jsonify({"msg": str(e)}), 401


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Оновлює access_token, використовуючи refresh_token з cookie."""
    current_user_id = get_jwt_identity()
    user_repo = get_user_repo()
    auth_service = AuthService(user_repo)
    user = auth_service.get_current_user(current_user_id)

    new_tokens = auth_service.refresh(user)

    response = make_response(jsonify({"msg": "Токен успішно оновлено"}))

    set_access_cookies(response, new_tokens["tokens"]["access_token"])

    return response, 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    current_user_id = get_jwt_identity()
    jwt = get_jwt()
    if jwt.get("type") != "user":
        return jsonify({"msg": "Ти маєш бути користувачем"}), 418
    user_repo = get_user_repo()
    auth_service = AuthService(user_repo)
    current_user = auth_service.get_current_user(current_user_id)

    return jsonify({"user": current_user.to_dict()}), 200


@auth_bp.route("/me/preferences", methods=["PUT"])
@jwt_required()
def update_preferences():
    """Оновлює налаштування (preferences) поточного користувача"""
    current_user_id = get_jwt_identity()
    data = request.get_json()

    if data is None:
        return jsonify({"msg": "Тіло запиту не може бути порожнім"}), 400

    user_repo = get_user_repo()
    auth_service = AuthService(user_repo)
    current_user = auth_service.get_current_user(current_user_id)

    try:
        updated_user = user_repo.update(current_user, {"preferences": data})
        
        return jsonify({"user": updated_user.to_dict()}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@auth_bp.route("/logout", methods=["POST"])
def logout():
    response = make_response(jsonify({"msg": "Успішний вихід"}))
    unset_jwt_cookies(response)
    return response, 200
