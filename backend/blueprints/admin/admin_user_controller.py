from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from middleware.auth_middleware import admin_token_required
from repositories import get_admin_repo

admin_user_bp = Blueprint("admin_user", __name__)


@admin_user_bp.route("/", methods=["GET"])
@admin_token_required
def get_all_admin_users(current_admin):
    """Отримує всіх адміністраторів"""
    try:
        admin_repo = get_admin_repo()
        admin_users = admin_repo.get_all()

        result = []
        for admin in admin_users:
            result.append(admin.to_dict())

        return jsonify({"admin_users": result, "total": len(result)}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@admin_user_bp.route("/<int:admin_id>", methods=["GET"])
@admin_token_required
def get_admin_user(current_admin, admin_id):
    """Отримує адміністратора за ID"""
    try:
        admin_repo = get_admin_repo()
        admin = admin_repo.get_by(id=admin_id)
        if not admin:
            return jsonify({"msg": "Адміністратора не знайдено"}), 404

        return jsonify(admin.to_dict()), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@admin_user_bp.route("/<int:admin_id>", methods=["PUT"])
@admin_token_required
def update_admin_user(current_admin, admin_id):
    """Оновлює адміністратора"""
    data = request.get_json()

    try:
        admin_repo = get_admin_repo()
        admin = admin_repo.get_by(id=admin_id)
        if not admin:
            return jsonify({"msg": "Адміністратора не знайдено"}), 404

        if current_admin.id == admin_id:
            return jsonify({"msg": "Ви не можете змінити самого себе"}), 403

        update_data = {}
        updatable_fields = ["email"]

        for field in updatable_fields:
            if field in data:
                if field in ["email"]:
                    existing = admin_repo.get_by(**{field: data.get(field)})
                    if existing and existing.id != admin_id:
                        return (
                            jsonify({"msg": f"Користувач з таким {field} вже існує"}),
                            400,
                        )
                update_data[field] = data.get(field)

        updated_user = admin_repo.update(admin, update_data)

        return jsonify(updated_user.to_dict()), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@admin_user_bp.route("/<int:admin_id>", methods=["DELETE"])
@admin_token_required
def delete_admin_user(current_admin, admin_id):
    """Видаляє адміністратора"""
    try:

        if current_admin.id == admin_id:
            return jsonify({"msg": "Ви не можете видалити свій власний аккаунт"}), 403

        admin_repo = get_admin_repo()
        admin = admin_repo.get_by(id=admin_id)
        if not admin:
            return jsonify({"msg": "Адміністратора не знайдено"}), 404

        admin_repo.delete(admin)
        return jsonify({"msg": "Адміністратора видалено"}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@admin_user_bp.route("/<int:admin_id>/change-password", methods=["PUT"])
@admin_token_required
def change_admin_password(current_admin, admin_id):
    """Змінює пароль адміністратора"""
    data = request.get_json()

    if not data.get("new_password"):
        return jsonify({"msg": "Новий пароль є обов'язковим"}), 400

    if len(data.get("new_password")) < 6:
        return jsonify({"msg": "Пароль повинен містити мінімум 6 символів"}), 400

    try:
        admin_repo = get_admin_repo()
        user = admin_repo.get_by(id=admin_id)
        if not user:
            return jsonify({"msg": "Адміністратора не знайдено"}), 404

        hashed_password = generate_password_hash(data.get("new_password"))
        admin_repo.update(user, {"password": hashed_password})

        return jsonify({"msg": "Пароль успішно змінено"}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500
