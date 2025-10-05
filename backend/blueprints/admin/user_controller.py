from flask import Blueprint, request, jsonify
from middleware.auth_middleware import admin_token_required
from repositories import get_user_repo, get_subscription_repo
from services.subscribtion_service import SubscriptionService

user_bp = Blueprint("user", __name__)


@user_bp.route("/", methods=["GET"])
@admin_token_required
def get_all_users(current_admin):
    """Отримує всіх користувачів"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    try:
        user_repo = get_user_repo()
        users = user_repo.get_all()

        # Простий варіант пагінації
        start = (page - 1) * per_page
        end = start + per_page
        paginated_users = users[start:end]

        result = [user.to_dict() for user in paginated_users]
        return (
            jsonify(
                {
                    "users": result,
                    "page": page,
                    "per_page": per_page,
                    "total": len(users),
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@user_bp.route("/<int:user_id>", methods=["GET"])
@admin_token_required
def get_user(current_admin, user_id):
    """Отримує користувача за ID"""
    try:
        user_repo = get_user_repo()
        user = user_repo.get_by(id=user_id)
        if not user:
            return jsonify({"msg": "Користувача не знайдено"}), 404

        user_data = user.to_dict()

        # Додаємо інформацію про підписки
        subscription_service = SubscriptionService(get_subscription_repo())
        current_subscription = subscription_service.get_current_subscription(user_id)
        user_data["current_subscription"] = (
            current_subscription.to_dict() if current_subscription else None
        )

        return jsonify(user_data), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@user_bp.route("/<int:user_id>", methods=["PUT"])
@admin_token_required
def update_user(current_admin, user_id):
    """Оновлює користувача"""
    data = request.get_json()

    try:
        user_repo = get_user_repo()
        user = user_repo.get_by(id=user_id)
        if not user:
            return jsonify({"msg": "Користувача не знайдено"}), 404

        update_data = {}
        updatable_fields = ["username", "email", "preferences"]
        for field in updatable_fields:
            if field in data:
                # Перевіряємо унікальність email та username
                if field in ["email", "username"]:
                    existing = user_repo.get_by(**{field: data.get(field)})
                    if existing and existing.id != user_id:
                        return (
                            jsonify({"msg": f"Користувач з таким {field} вже існує"}),
                            400,
                        )
                update_data[field] = data.get(field)

        updated_user = user_repo.update(user, update_data)
        return jsonify(updated_user.to_dict()), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@user_bp.route("/<int:user_id>", methods=["DELETE"])
@admin_token_required
def delete_user(current_admin, user_id):
    """Видаляє користувача"""
    try:
        user_repo = get_user_repo()
        user = user_repo.get_by(id=user_id)
        if not user:
            return jsonify({"msg": "Користувача не знайдено"}), 404

        user_repo.delete(user)
        return jsonify({"msg": "Користувача видалено"}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@user_bp.route("/<int:user_id>/subscription", methods=["PUT"])
@admin_token_required
def update_user_subscription(current_admin, user_id):
    """Змінює підписку користувача"""
    data = request.get_json()

    if not data.get("plan_id"):
        return jsonify({"msg": "ID плану є обов'язковим"}), 400

    try:
        user_repo = get_user_repo()
        user = user_repo.get_by(id=user_id)
        if not user:
            return jsonify({"msg": "Користувача не знайдено"}), 404

        subscription_service = SubscriptionService(get_subscription_repo())
        subscription = subscription_service.subscribe(user_id, data.get("plan_id"))

        return (
            jsonify(
                {"msg": "Підписку оновлено", "subscription": subscription.to_dict()}
            ),
            200,
        )
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@user_bp.route("/<int:user_id>/subscriptions/history", methods=["GET"])
@admin_token_required
def get_user_subscription_history(current_admin, user_id):
    """Отримує історію підписок користувача"""
    try:
        user_repo = get_user_repo()
        user = user_repo.get_by(id=user_id)
        if not user:
            return jsonify({"msg": "Користувача не знайдено"}), 404

        subscription_service = SubscriptionService(get_subscription_repo())
        history = subscription_service.get_subscription_history(user_id)

        result = [sub.to_dict() for sub in history] if history else []
        return jsonify({"subscriptions": result}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500
