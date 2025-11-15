from flask import Blueprint, request, jsonify
from middleware.auth_middleware import token_required
from repositories import get_subscription_repo
from services.subscribtion_service import SubscriptionService

subscription_bp = Blueprint("subscription", __name__)


@subscription_bp.route("/", methods=["GET"])
def get_plans():
    plans = SubscriptionService(get_subscription_repo()).list_plans()
    result = [plan.to_dict() for plan in plans]
    return jsonify(result), 200


@subscription_bp.route("/subscribe", methods=["POST"])
@token_required
def subscribe(current_user):
    data = request.get_json()
    plan_id = data.get("plan_id")
    if not plan_id:
        return jsonify(msg="plan_id is required"), 400

    sub = SubscriptionService(get_subscription_repo()).subscribe(
        current_user.id, plan_id
    )
    return jsonify(sub.to_dict()), 201


@subscription_bp.route("/me", methods=["GET"])
@token_required
def my_subscription(current_user):
    sub = SubscriptionService(get_subscription_repo()).get_current_subscription(
        current_user.id
    )
    if not sub:
        raise ValueError("У вас немає активної підписки")
    return jsonify(sub.to_dict()), 200


@subscription_bp.route("/history", methods=["GET"])
@token_required
def subscription_history(current_user):
    subs = SubscriptionService(get_subscription_repo()).get_subscription_history(
        current_user.id
    )
    if not subs:
        return jsonify([]), 200
    result = [sub.to_dict() for sub in subs]
    return jsonify(result), 200
