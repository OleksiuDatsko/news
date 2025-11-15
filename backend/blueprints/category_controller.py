from flask import Blueprint, jsonify
from repositories import get_category_repo

category_bp = Blueprint("category", __name__)


@category_bp.route("/", methods=["GET"])
def get_all_categories():
    """Отримує список всіх категорій"""
    category_repo = get_category_repo()
    categories = category_repo.get_all()
    result = [category.to_dict() for category in categories]
    return jsonify({"categories": result, "total": len(result)}), 200


@category_bp.route("/slug/<string:slug>", methods=["GET"])
def get_category_by_slug(slug):
    """Отримує одну категорію за її 'slug'"""
    category_repo = get_category_repo()
    category = category_repo.get_by(slug=slug)

    if not category:
        raise ValueError("Категорію не знайдено")

    return jsonify(category.to_dict()), 200
