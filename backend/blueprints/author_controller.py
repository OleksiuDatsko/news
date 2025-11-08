from flask import Blueprint, g, request, jsonify
from models.user import User
from middleware.auth_middleware import token_optional, token_required
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
    
@author_bp.route("/followed", methods=["GET"])
@token_required
def get_followed_authors(current_user: User):
    """Отримує список авторів, на яких підписаний поточний користувач"""
    try:
        followed = current_user.followed_authors
        result = [author.to_dict() for author in followed]
        return jsonify({"authors": result, "total": len(result)}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500    

@author_bp.route("/<int:author_id>/toggle-follow", methods=["POST"])
@token_required
def toggle_follow_author(current_user: User, author_id: int):
    """
    Додає або видаляє підписку на автора для поточного користувача.
    Це "акуратна" версія, що працює з M2M-таблицею.
    """
    author_repo = get_author_repo()
    author = author_repo.get_by(id=author_id)
    if not author:
        return jsonify({"msg": "Автора не знайдено"}), 404

    is_following = False
    
    if author in current_user.followed_authors:
        current_user.followed_authors.remove(author)
        is_following = False
    else:
        current_user.followed_authors.append(author)
        is_following = True

    try:
        g.db_session.commit() 
        return jsonify({
            "msg": "Статус підписки оновлено", 
            "is_following": is_following
        }), 200
    except Exception as e:
        g.db_session.rollback()
        return jsonify({"msg": f"Помилка оновлення: {str(e)}"}), 500