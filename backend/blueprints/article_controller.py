from flask import Blueprint, request, jsonify
from middleware.ads_middleware import ads_injector
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
@ads_injector(ad_type="sidebar")
def get_articles(current_user, ads=[]):
    """Отримує список статей"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    status = request.args.get("status")
    category_id = request.args.get("category", type=int)
    category_slug = request.args.get("category_slug", type=str)
    filters = {}
    if status:
        filters["status"] = status
    if category_id:
        filters["category_id"] = category_id
    if not getattr(current_user, "permissions", {}).get("exclusive_content", False):
        filters["is_exclusive"] = False
    if category_slug:
        filters["category_slug"] = category_slug

    article_repo = get_article_repo()
    article_service = ArticleService(article_repo)

    articles, total = article_service.get_articles(
        page=page, per_page=per_page, filters=filters
    )
    result = [article.to_dict(metadata=True) for article in articles]
    return (
        jsonify(
            {
                "articles": result,
                "ads": ads,
                "page": page,
                "per_page": per_page,
                "total": total,
            }
        ),
        200,
    )


@article_bp.route("/recommended", methods=["GET"])
@token_required
@ads_injector(ad_type="inline")
def get_recommended_articles(current_user, ads=[]):
    """Отримує рекомендовані статті на основі уподобань ТА АКТИВНОСТІ користувача"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)
    status = request.args.get("satus", "published", type=str)
    current_article_id = request.args.get("article_id", type=int)

    article_repo = get_article_repo()
    article_service = ArticleService(article_repo)

    filters = {"status": status}

    preferences = current_user.preferences or {}
    fav_category_slugs = preferences.get("favorite_categories", [])

    if not getattr(current_user, "permissions", {}).get("exclusive_content", False):
        filters["is_exclusive"] = False

    articles, total = article_service.get_recommended_articles(
        user_id=current_user.id,
        page=page,
        per_page=per_page,
        favorite_category_slugs=fav_category_slugs,
        filters=filters,
        current_article_id=current_article_id,
    )

    result = [article.to_dict(metadata=True) for article in articles]
    return (
        jsonify(
            {
                "articles": result,
                "ads": ads,
                "page": page,
                "per_page": per_page,
                "total": total,
            }
        ),
        200,
    )


@article_bp.route("/search", methods=["GET"])
@token_optional
def search_articles(current_user):
    query = request.args.get("q")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")

    if not query:
        return jsonify({"msg": "Параметр 'q' є обов'язковим"}), 400

    article_repo = get_article_repo()
    article_service = ArticleService(article_repo)

    user_permissions = current_user.permissions if current_user else {}

    articles, total = article_service.search_articles(
        query,
        page,
        per_page,
        user_permissions=user_permissions,
        date_from=date_from,
        date_to=date_to,
    )

    result = [article.to_dict(metadata=True) for article in articles]

    return (
        jsonify(
            {
                "articles": result,
                "query": query,
                "page": page,
                "per_page": per_page,
                "total": total,
                "date_from": date_from,
                "date_to": date_to,
            }
        ),
        200,
    )


@article_bp.route("/<int:article_id>", methods=["GET"])
@token_optional
@ads_injector(ad_type="banner")
def get_article(current_user, ads, article_id):
    """Отримує статтю за ID"""
    article_repo = get_article_repo()
    article_service = ArticleService(article_repo)

    if current_user:
        article = article_service.get_article_by_id(article_id, current_user.id)
    else:
        article = article_service.get_article_by_id(article_id)

    if not getattr(current_user, "permissions", {}).get(
        "exclusive_content", False
    ) and article.get("is_exclusive", False):
        raise PermissionError("Недостатньо прав для доступу до цього ресурсу")

    return jsonify({**article, "ads": ads}), 200


@article_bp.route("/<int:article_id>/impression", methods=["POST"])
@token_optional
def record_article_impression(current_user, article_id):
    """Реєструє показ картки статті."""
    data = request.get_json() or {}
    article_repo = get_article_repo()
    article_service = ArticleService(article_repo)

    success = article_service.record_article_impression(
        article_id=article_id,
        user_id=current_user.id if current_user else None,
        session_id=data.get("session_id"),
        ip_address=request.remote_addr,
    )

    if success:
        return jsonify({"msg": "Показ статті зареєстровано"}), 200
    else:
        return jsonify({"msg": "Помилка при реєстрації показу"}), 500


@article_bp.route("/<int:article_id>/save", methods=["POST"])
@token_required
@permission_required("save_article")
def save_article(current_user, article_id):
    """Зберігає статтю"""
    article_repo = get_article_repo()
    article_service = ArticleService(article_repo)

    result = article_service.save_article(current_user.id, article_id)
    return jsonify(result), 200


@article_bp.route("/<int:article_id>/unsave", methods=["POST"])
@token_required
@permission_required("save_article")
def unsave_article(current_user, article_id):
    """Прибирає статтю зі збережених"""
    article_repo = get_article_repo()
    article_service = ArticleService(article_repo)

    result = article_service.unsave_article(current_user.id, article_id)
    return jsonify(result), 200


@article_bp.route("/<int:article_id>/toggle-save", methods=["POST"])
@token_required
@permission_required("save_article")
def toggle_save_article(current_user, article_id):
    """Перемикає статус збереження статті"""
    article_repo = get_article_repo()
    article_service = ArticleService(article_repo)

    result = article_service.toggle_save_article(current_user.id, article_id)
    return jsonify(result), 200


@article_bp.route("/<int:article_id>/toggle-like", methods=["POST"])
@token_required
def toggle_like_article(current_user):
    """Перемикає статус лайка статті"""
    if current_user.is_admin:
        return jsonify({"msg": "Адмін не може оцінювати статті"}), 403

    article_repo = get_article_repo()
    article_service = ArticleService(article_repo)

    result = article_service.toggle_like_article(current_user.id, article_id)
    return jsonify(result), 200


@article_bp.route("/saved", methods=["GET"])
@token_required
def get_saved_articles(current_user):
    """Отримує збережені статті користувача"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    get_all_ids = request.args.get("ids", False, type=bool)

    article_repo = get_article_repo()
    article_service = ArticleService(article_repo)

    articles = article_service.get_saved_articles(current_user.id, page, per_page)
    if get_all_ids:
        articles = [article.get("id") for article in articles]
    return jsonify(articles), 200


@article_bp.route("/liked", methods=["GET"])
@token_required
def get_liked_articles(current_user):
    """Отримує статті, які лайкнув користувач"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    article_repo = get_article_repo()
    article_service = ArticleService(article_repo)

    articles = article_service.get_liked_articles(current_user.id, page, per_page)
    return jsonify(articles), 200
