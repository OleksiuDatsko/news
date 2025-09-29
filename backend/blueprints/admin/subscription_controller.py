from flask import Blueprint, request, jsonify
from middleware.auth_middleware import admin_token_required
from repositories import get_subscription_repo
from services.subscribtion_service import SubscriptionService

subscription_bp = Blueprint("subscription", __name__)


@subscription_bp.route("/", methods=["GET"])
@admin_token_required
def get_all_plans(current_admin):
    """Отримує всі плани підписки"""
    try:
        subscription_service = SubscriptionService(get_subscription_repo())
        plans = subscription_service.list_plans()
        result = [plan.to_dict() for plan in plans]
        return jsonify({"plans": result, "total": len(result)}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@subscription_bp.route("/", methods=["POST"])
@admin_token_required
def create_plan(current_admin):
    """Створює новий план підписки"""
    data = request.get_json()

    if not data.get("name"):
        return jsonify({"msg": "Назва плану є обов'язковою"}), 400
    if not data.get("permissions"):
        return jsonify({"msg": "Дозволи є обов'язковими"}), 400

    try:
        subscription_repo = get_subscription_repo()
        plan = subscription_repo.create(
            {
                "name": data.get("name"),
                "permissions": data.get("permissions"),
                "price_per_month": data.get("price_per_month"),
                "description": data.get("description"),
            }
        )
        return jsonify(plan.to_dict()), 201
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@subscription_bp.route("/<int:plan_id>", methods=["GET"])
@admin_token_required
def get_plan(current_admin, plan_id):
    """Отримує план підписки за ID"""
    try:
        subscription_repo = get_subscription_repo()
        plan = subscription_repo.get_by(id=plan_id)
        if not plan:
            return jsonify({"msg": "План не знайдено"}), 404
        return jsonify(plan.to_dict()), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@subscription_bp.route("/<int:plan_id>", methods=["PUT"])
@admin_token_required
def update_plan(current_admin, plan_id):
    """Оновлює план підписки"""
    data = request.get_json()

    try:
        subscription_repo = get_subscription_repo()
        plan = subscription_repo.get_by(id=plan_id)
        if not plan:
            return jsonify({"msg": "План не знайдено"}), 404

        update_data = {}
        if data.get("name"):
            update_data["name"] = data.get("name")
        if data.get("permissions"):
            update_data["permissions"] = data.get("permissions")
        if "price_per_month" in data:
            update_data["price_per_month"] = data.get("price_per_month")
        if "description" in data:
            update_data["description"] = data.get("description")

        updated_plan = subscription_repo.update(plan, update_data)
        return jsonify(updated_plan.to_dict()), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@subscription_bp.route("/<int:plan_id>", methods=["DELETE"])
@admin_token_required
def delete_plan(current_admin, plan_id):
    """Видаляє план підписки"""
    try:
        subscription_repo = get_subscription_repo()
        plan = subscription_repo.get_by(id=plan_id)
        if not plan:
            return jsonify({"msg": "План не знайдено"}), 404

        subscription_repo.delete(plan)
        return jsonify({"msg": "План видалено"}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500
