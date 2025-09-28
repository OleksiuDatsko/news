from flask import Blueprint, request, jsonify
from middleware.auth_middleware import (
    token_optional,
    token_required,
    permission_required,
)
from repositories import get_article_repo
from services.article_service import ArticleService

article_bp = Blueprint("article", __name__)


@article_bp.route("/", methods=["GET"])
@token_optional
def get_articles(current_user):
    """Отримує список статей"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    status = request.args.get("status")
    category_id = request.args.get("category", type=int)
    filters = {}
    if status:
        filters["status"] = status
    if category_id:
        filters["category_id"] = category_id
    if current_user and not current_user.permissions.get("exclusive_content", False):
        filters["is_exclusive"] = False

    article_repo = get_article_repo()
    article_service = ArticleService(article_repo)

    try:
        articles = article_service.get_articles(
            page=page, per_page=per_page, filters=filters
        )
        result = [article.to_dict(metadata=True) for article in articles]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@article_bp.route("/<int:article_id>", methods=["GET"])
@token_optional
def get_article(current_user, article_id):
    """Отримує статтю за ID"""
    article_repo = get_article_repo()
    article_service = ArticleService(article_repo)

    try:
        if current_user:
            article = article_service.get_article_by_id(article_id, current_user.id)
        else:
            article = article_service.get_article_by_id(article_id)
        if (
            current_user
            and not current_user.permissions.get("exclusive_content", False)
            and article.get("is_exclusive", False)
        ):
            return (
                jsonify({"msg": "Недостатньо прав для доступу до цього ресурсу"}),
                403,
            )
        return jsonify(article), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404


@article_bp.route("/<int:article_id>/save", methods=["POST"])
@token_required
@permission_required("save_article")
def save_article(current_user, article_id):
    """Зберігає статтю"""
    article_repo = get_article_repo()
    article_service = ArticleService(article_repo)

    try:
        result = article_service.save_article(current_user.id, article_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404


@article_bp.route("/<int:article_id>/unsave", methods=["POST"])
@token_required
@permission_required("save_article")
def unsave_article(current_user, article_id):
    """Прибирає статтю зі збережених"""
    article_repo = get_article_repo()
    article_service = ArticleService(article_repo)

    try:
        result = article_service.unsave_article(current_user.id, article_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404


@article_bp.route("/<int:article_id>/toggle-save", methods=["POST"])
@token_required
@permission_required("save_article")
def toggle_save_article(current_user, article_id):
    """Перемикає статус збереження статті"""
    article_repo = get_article_repo()
    article_service = ArticleService(article_repo)

    try:
        result = article_service.toggle_save_article(current_user.id, article_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404


@article_bp.route("/saved", methods=["GET"])
@token_required
def get_saved_articles(current_user):
    """Отримує збережені статті користувача"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    article_repo = get_article_repo()
    article_service = ArticleService(article_repo)

    try:
        articles = article_service.get_saved_articles(current_user.id, page, per_page)
        return jsonify(articles), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500
