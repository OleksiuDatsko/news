from flask import Blueprint, request, jsonify
from middleware.auth_middleware import admin_token_required
from repositories import get_subscription_repo

subscription_bp = Blueprint("subscription", __name__)


@subscription_bp.route("/", methods=["GET"])
@admin_token_required
def get_all_plans(current_admin):
    """Отримує всі плани підписок"""
    subscription_repo = get_subscription_repo()
    plans = subscription_repo.get_all()
    result = [plan.to_dict() for plan in plans]
    return jsonify({"plans": result, "total": len(result)}), 200


@subscription_bp.route("/", methods=["POST"])
@admin_token_required
def create_plan(current_admin):
    """Створює новий план підписки"""
    data = request.get_json()

    if not data.get("name"):
        return jsonify({"msg": "Назва плану є обов'язковою"}), 400
    if "permissions" not in data:
        return jsonify({"msg": "Поле 'permissions' є обов'язковим"}), 400

    subscription_repo = get_subscription_repo()
    plan = subscription_repo.create(
        {
            "name": data.get("name"),
            "permissions": data.get("permissions"),
            "price_per_month": data.get("price_per_month", 0),
            "description": data.get("description", ""),
        }
    )
    return jsonify(plan.to_dict()), 201


@subscription_bp.route("/<int:plan_id>", methods=["GET"])
@admin_token_required
def get_plan(current_admin, plan_id):
    """Отримує план за ID"""
    subscription_repo = get_subscription_repo()
    plan = subscription_repo.get_by(id=plan_id)
    if not plan:
        raise ValueError("План не знайдено")
    return jsonify(plan.to_dict()), 200


@subscription_bp.route("/<int:plan_id>", methods=["PUT"])
@admin_token_required
def update_plan(current_admin, plan_id):
    """Оновлює план підписки"""
    data = request.get_json()

    subscription_repo = get_subscription_repo()
    plan = subscription_repo.get_by(id=plan_id)
    if not plan:
        raise ValueError("План не знайдено")

    update_data = {}
    updatable_fields = [
        "name",
        "permissions",
        "price_per_month",
        "description",
    ]
    for field in updatable_fields:
        if field in data:
            update_data[field] = data.get(field)

    updated_plan = subscription_repo.update(plan, update_data)
    return jsonify(updated_plan.to_dict()), 200


@subscription_bp.route("/<int:plan_id>", methods=["DELETE"])
@admin_token_required
def delete_plan(current_admin, plan_id):
    """Видаляє план підписки"""
    subscription_repo = get_subscription_repo()
    plan = subscription_repo.get_by(id=plan_id)
    if not plan:
        raise ValueError("План не знайдено")

    subscription_repo.delete(plan)
    return jsonify({"msg": "План видалено"}), 200
