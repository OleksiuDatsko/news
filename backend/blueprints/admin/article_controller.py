from flask import Blueprint, g, request, jsonify
from middleware.auth_middleware import admin_token_required
from models.article import Article
from repositories import get_article_repo
from services.article_service import ArticleService
from services.notification_service import notification_service

article_bp = Blueprint("article", __name__)


@article_bp.route("/", methods=["GET"])
@admin_token_required
def get_all_articles(current_admin):
    """Отримує всі статті з можливістю фільтрації"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 1000, type=int)
    status = request.args.get("status")
    category_id = request.args.get("category", type=int)

    filters = {}
    if status:
        filters["status"] = status
    if category_id:
        filters["category_id"] = category_id

    article_service = ArticleService(get_article_repo())
    articles, total = article_service.get_articles(
        page=page, per_page=per_page, filters=filters
    )
    result = [article.to_dict(metadata=True) for article in articles]
    return (
        jsonify(
            {"articles": result, "page": page, "per_page": per_page, "total": total}
        ),
        200,
    )


@article_bp.route("/", methods=["POST"])
@admin_token_required
def create_article(current_admin):
    """Створює нову статтю"""
    data = request.get_json()

    required_fields = ["title", "content", "author_id"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"msg": f"{field} є обов'язковим"}), 400

    article_repo = get_article_repo()
    article = article_repo.create(
        {
            "title": data.get("title"),
            "content": data.get("content"),
            "author_id": data.get("author_id"),
            "category_id": data.get("category_id"),
            "status": data.get("status", "draft"),
            "is_exclusive": data.get("is_exclusive", False),
            "is_breaking": data.get("is_breaking", False),
        }
    )
    return jsonify(article.to_dict()), 201


@article_bp.route("/<int:article_id>", methods=["GET"])
@admin_token_required
def get_article(current_admin, article_id):
    """Отримує статтю за ID"""
    article_service = ArticleService(get_article_repo())
    article = article_service.get_article_by_id(article_id)
    return jsonify(article), 200


@article_bp.route("/<int:article_id>", methods=["PUT"])
@admin_token_required
def update_article(current_admin, article_id):
    """Оновлює статтю"""
    data = request.get_json()

    article_repo = get_article_repo()
    article = article_repo.get_by(id=article_id)
    if not article:
        raise ValueError("Статтю не знайдено")

    old_status = article.status
    new_status = data.get("status", old_status)

    if old_status != "published" and new_status == "published":
        for field in data:
            if hasattr(article, field):
                setattr(article, field, data[field])

        _ = article.category
        notification_service.notify(article, g.db_session)

    update_data = {}
    updatable_fields = [
        "title",
        "content",
        "author_id",
        "category_id",
        "status",
        "is_exclusive",
        "is_breaking",
    ]
    for field in updatable_fields:
        if field in data:
            update_data[field] = data.get(field)

    updated_article = article_repo.update(article, update_data)
    return jsonify(updated_article.to_dict()), 200


@article_bp.route("/<int:article_id>", methods=["DELETE"])
@admin_token_required
def delete_article(current_admin, article_id):
    """Видаляє статтю"""
    article_repo = get_article_repo()
    article = article_repo.get_by(id=article_id)
    if not article:
        raise ValueError("Статтю не знайдено")

    article_repo.delete(article)
    return jsonify({"msg": "Статтю видалено"}), 200


@article_bp.route("/<int:article_id>/status", methods=["PUT"])
@admin_token_required
def update_article_status(current_admin, article_id):
    """Оновлює статус статті"""
    data = request.get_json()
    new_status = data.get("status")

    if not new_status:
        return jsonify({"msg": "Статус є обов'язковим"}), 400

    valid_statuses = ["draft", "published", "archived"]
    if new_status not in valid_statuses:
        return (
            jsonify(
                {"msg": f"Невірний статус. Допустимі: {', '.join(valid_statuses)}"}
            ),
            400,
        )

    article_repo = get_article_repo()
    article = article_repo.get_by(id=article_id)
    if not article:
        raise ValueError("Статтю не знайдено")

    old_status = article.status
    if old_status != "published" and new_status == "published":
        article.status = new_status
        _ = article.category
        notification_service.notify(article, g.db_session)

    updated_article = article_repo.update(article, {"status": data.get("status")})
    return jsonify(updated_article.to_dict()), 200
