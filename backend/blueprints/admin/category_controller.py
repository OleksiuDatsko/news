from flask import Blueprint, request, jsonify
from middleware.auth_middleware import admin_token_required
from repositories import get_category_repo

category_bp = Blueprint("category", __name__)


@category_bp.route("/", methods=["GET"])
@admin_token_required
def get_all_categories(current_admin):
    """Отримує всі категорії"""
    try:
        category_repo = get_category_repo()
        categories = category_repo.get_all()
        result = [category.to_dict() for category in categories]
        return jsonify({"categories": result, "total": len(result)}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@category_bp.route("/", methods=["POST"])
@admin_token_required
def create_category(current_admin):
    """Створює нову категорію"""
    data = request.get_json()

    if not data.get("name"):
        return jsonify({"msg": "Назва категорії є обов'язковою"}), 400

    try:
        category_repo = get_category_repo()
        category = category_repo.create(
            {
                "name": data.get("name"),
                "description": data.get("description"),
                "is_searchable": data.get("is_searchable", True),
            }
        )
        return jsonify(category.to_dict()), 201
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@category_bp.route("/<int:category_id>", methods=["GET"])
@admin_token_required
def get_category(current_admin, category_id):
    """Отримує категорію за ID"""
    try:
        category_repo = get_category_repo()
        category = category_repo.get_by(id=category_id)
        if not category:
            return jsonify({"msg": "Категорію не знайдено"}), 404
        return jsonify(category.to_dict()), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@category_bp.route("/<int:category_id>", methods=["PUT"])
@admin_token_required
def update_category(current_admin, category_id):
    """Оновлює категорію"""
    data = request.get_json()

    try:
        category_repo = get_category_repo()
        category = category_repo.get_by(id=category_id)
        if not category:
            return jsonify({"msg": "Категорію не знайдено"}), 404

        update_data = {}
        if data.get("name"):
            update_data["name"] = data.get("name")
        if "description" in data:
            update_data["description"] = data.get("description")
        if "is_searchable" in data:
            update_data["is_searchable"] = data.get("is_searchable")

        updated_category = category_repo.update(category, update_data)
        return jsonify(updated_category.to_dict()), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@category_bp.route("/<int:category_id>", methods=["DELETE"])
@admin_token_required
def delete_category(current_admin, category_id):
    """Видаляє категорію"""
    try:
        category_repo = get_category_repo()
        category = category_repo.get_by(id=category_id)
        if not category:
            return jsonify({"msg": "Категорію не знайдено"}), 404

        category_repo.delete(category)
        return jsonify({"msg": "Категорію видалено"}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500
