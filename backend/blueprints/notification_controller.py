from flask import Blueprint, jsonify, request
from models.push_subscription import PushSubscription
from middleware.auth_middleware import token_required
from repositories import get_notification_repo

notification_bp = Blueprint("notification", __name__)

@notification_bp.route("/", methods=["GET"])
@token_required
def get_notifications(current_user):
    """Отримує останні 10 непрочитаних сповіщень для поточного користувача."""
    if current_user.is_admin:
         return jsonify({"notifications": [], "unread_count": 0}), 200

    repo = get_notification_repo()
    unread_notifications = repo.get_unread_by_user(current_user.id, limit=10)
    
    result = [n.to_dict() for n in unread_notifications]
    return jsonify({
        "notifications": result,
        "unread_count": len(result)
    }), 200

@notification_bp.route("/<int:notification_id>/read", methods=["POST"])
@token_required
def mark_as_read(current_user, notification_id):
    """Позначає одне сповіщення як прочитане."""
    if current_user.is_admin:
        return jsonify({"msg": "Адмін не має сповіщень"}), 403

    repo = get_notification_repo()
    notification = repo.mark_as_read(notification_id, current_user.id)
    
    if not notification:
        return jsonify({"msg": "Сповіщення не знайдено або належить іншому користувачу"}), 404
        
    return jsonify(notification.to_dict()), 200

@notification_bp.route("/read-all", methods=["POST"])
@token_required
def mark_all_as_read(current_user):
    """Позначає всі сповіщення користувача як прочитані."""
    if current_user.is_admin:
        return jsonify({"msg": "Адмін не має сповіщень"}), 403
        
    repo = get_notification_repo()
    repo.mark_all_as_read(current_user.id)
    
    return jsonify({"msg": "Всі сповіщення позначено як прочитані"}), 200

@notification_bp.route("/all", methods=["GET"])
@token_required
def get_all_notifications(current_user):
    """Отримує ВСІ сповіщення для користувача з пагінацією."""
    if current_user.is_admin:
         return jsonify({"notifications": [], "total": 0, "page": 1, "per_page": 10}), 200

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    
    repo = get_notification_repo()
    notifications, total = repo.get_all_by_user(
        current_user.id, page=page, per_page=per_page
    )
    
    result = [n.to_dict() for n in notifications]
    return jsonify({
        "notifications": result,
        "total": total,
        "page": page,
        "per_page": per_page
    }), 200
    
@notification_bp.route("/subscribe", methods=["POST"])
@token_required
def subscribe_to_push(current_user):
    """
    Підписує користувача на push-сповіщення.
    """
    data = request.get_json()
    if not data or not data.get("endpoint"):
        return jsonify({"msg": "Необхідні дані підписки"}), 400

    from flask import g    
    existing = g.db_session.query(PushSubscription).filter_by(endpoint=data["endpoint"]).first()
    if existing:
        return jsonify({"msg": "Підписка вже існує"}), 200

    try:
        sub = PushSubscription(
            user_id=current_user.id,
            endpoint=data["endpoint"],
            p256dh=data["keys"]["p256dh"],
            auth=data["keys"]["auth"]
        )
        g.db_session.add(sub)
        g.db_session.commit()
        
        return jsonify({"msg": "Підписка успішна"}), 201
    except Exception as e:
        g.db_session.rollback()
        return jsonify({"msg": str(e)}), 500