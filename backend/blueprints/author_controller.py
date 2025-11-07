from flask import Blueprint, request, jsonify
from middleware.auth_middleware import token_optional
from repositories import get_author_repo, get_article_repo
from services.article_service import ArticleService

author_bp = Blueprint("author", __name__)


@author_bp.route("/<int:author_id>", methods=["GET"])
def get_author(author_id):
    """Отримує публічну інформацію про автора за ID"""
    try:
        author_repo = get_author_repo()
        author = author_repo.get_by(id=author_id)
        if not author:
            return jsonify({"msg": "Автора не знайдено"}), 404
        
        return jsonify(author.to_dict()), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@author_bp.route("/<int:author_id>/articles", methods=["GET"])
@token_optional
def get_author_articles(current_user, author_id):
    """Отримує опубліковані статті автора"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    filters = {
        "author_id": author_id,
        "status": "published"
    }

    if not getattr(current_user, "permissions", {}).get("exclusive_content", False):
        filters["is_exclusive"] = False

    article_repo = get_article_repo()
    article_service = ArticleService(article_repo)

    try:
        articles, total = article_service.get_articles(
            page=page, per_page=per_page, filters=filters
        )
        result = [article.to_dict(metadata=True) for article in articles]
        return (
            jsonify(
                {
                    "articles": result,
                    "page": page,
                    "per_page": per_page,
                    "total": total,
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"msg": str(e)}), 500