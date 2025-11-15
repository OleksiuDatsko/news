from flask import Blueprint, request, jsonify, g
from middleware.auth_middleware import token_required
from repositories import get_notification_repo
from models.push_subscription import PushSubscription

notification_bp = Blueprint("notification", __name__)


@notification_bp.route("/", methods=["GET"])
@token_required
def get_unread(current_user):
    """Отримує останні 5 непрочитаних сповіщень"""
    repo = get_notification_repo()
    notifications = repo.get_unread_by_user(current_user.id, limit=5)
    unread_count = (
        repo.db_session.query(repo.model)
        .filter_by(user_id=current_user.id, is_read=False)
        .count()
    )

    return (
        jsonify(
            {
                "notifications": [n.to_dict() for n in notifications],
                "unread_count": unread_count,
            }
        ),
        200,
    )


@notification_bp.route("/all", methods=["GET"])
@token_required
def get_all(current_user):
    """Отримує всі сповіщення з пагінацією"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    repo = get_notification_repo()
    notifications, total = repo.get_all_by_user(current_user.id, page, per_page)

    return (
        jsonify(
            {
                "notifications": [n.to_dict() for n in notifications],
                "total": total,
                "page": page,
                "per_page": per_page,
            }
        ),
        200,
    )


@notification_bp.route("/<int:notification_id>/read", methods=["POST"])
@token_required
def mark_as_read(current_user, notification_id):
    """Позначає одне сповіщення як прочитане"""
    repo = get_notification_repo()
    notification = repo.mark_as_read(notification_id, current_user.id)

    if not notification:
        raise ValueError("Сповіщення не знайдено або вже прочитано")

    return jsonify(notification.to_dict()), 200


@notification_bp.route("/read-all", methods=["POST"])
@token_required
def mark_all_read(current_user):
    """Позначає всі сповіщення як прочитані"""
    repo = get_notification_repo()
    repo.mark_all_as_read(current_user.id)
    return jsonify({"msg": "Всі сповіщення позначено як прочитані"}), 200


@notification_bp.route("/subscribe", methods=["POST"])
@token_required
def subscribe(current_user):
    """Підписує користувача на PUSH-сповіщення"""
    data = request.get_json()

    if not data or "endpoint" not in data:
        return jsonify({"msg": "Невірні дані підписки"}), 400

    endpoint = data["endpoint"]
    p256dh = data.get("keys", {}).get("p256dh")
    auth = data.get("keys", {}).get("auth")

    if not p256dh or not auth:
        return jsonify({"msg": "Ключі підписки відсутні"}), 400

    existing_sub = (
        g.db_session.query(PushSubscription).filter_by(endpoint=endpoint).first()
    )

    if existing_sub:
        if existing_sub.user_id != current_user.id:
            existing_sub.user_id = current_user.id
            g.db_session.commit()
        return jsonify({"msg": "Підписка вже існує"}), 200

    new_sub = PushSubscription(
        user_id=current_user.id, endpoint=endpoint, p256dh=p256dh, auth=auth
    )
    g.db_session.add(new_sub)
    g.db_session.commit()

    return jsonify({"msg": "Підписка успішно створена"}), 201
