from flask import Blueprint, jsonify
from repositories import get_category_repo

category_bp = Blueprint("category", __name__)


@category_bp.route("/", methods=["GET"])
def get_all_categories():
    """Отримує список всіх категорій"""
    try:
        category_repo = get_category_repo()
        categories = category_repo.get_all()
        result = [category.to_dict() for category in categories]
        return jsonify({"categories": result, "total": len(result)}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@category_bp.route("/slug/<string:slug>", methods=["GET"])
def get_category_by_slug(slug):
    """Отримує одну категорію за її 'slug'"""
    try:
        category_repo = get_category_repo()
        category = category_repo.get_by(slug=slug) 
        
        if not category:
            return jsonify({"msg": "Категорію не знайдено"}), 404
            
        return jsonify(category.to_dict()), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500