from flask import Blueprint, request, jsonify
from middleware.auth_middleware import admin_token_required
from repositories import get_author_repo, get_article_repo

author_bp = Blueprint("author", __name__)


@author_bp.route("/", methods=["GET"])
@admin_token_required
def get_all_authors(current_admin):
    """Отримує всіх авторів"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 1000, type=int)
    search = request.args.get("search", "")

    author_repo = get_author_repo()
    authors = author_repo.get_all()

    if search:
        search_lower = search.lower()
        authors = [
            author
            for author in authors
            if search_lower in author.first_name.lower()
            or search_lower in author.last_name.lower()
            or (author.bio and search_lower in author.bio.lower())
        ]

    start = (page - 1) * per_page
    end = start + per_page
    paginated_authors = [author.to_dict() for author in authors[start:end]]

    return (
        jsonify(
            {
                "authors": paginated_authors,
                "page": page,
                "per_page": per_page,
                "total": len(authors),
                "search": search,
            }
        ),
        200,
    )


@author_bp.route("/", methods=["POST"])
@admin_token_required
def create_author(current_admin):
    """Створює нового автора"""
    data = request.get_json()

    if not data.get("first_name"):
        return jsonify({"msg": "Ім'я є обов'язковим"}), 400
    if not data.get("last_name"):
        return jsonify({"msg": "Прізвище є обов'язковим"}), 400

    author_repo = get_author_repo()
    author = author_repo.create(
        {
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "bio": data.get("bio", ""),
        }
    )
    return jsonify(author.to_dict()), 201


@author_bp.route("/<int:author_id>", methods=["GET"])
@admin_token_required
def get_author(current_admin, author_id):
    """Отримує автора за ID з детальною інформацією"""
    author_repo = get_author_repo()
    author = author_repo.get_by(id=author_id)
    if not author:
        raise ValueError("Автора не знайдено")

    author_data = author.to_dict()

    recent_articles = sorted(author.articles, key=lambda x: x.created_at, reverse=True)[
        :5
    ]
    author_data["recent_articles"] = [
        {
            "id": article.id,
            "title": article.title,
            "status": article.status,
            "created_at": (
                article.created_at.isoformat() if article.created_at else None
            ),
            "views_count": article.views_count,
        }
        for article in recent_articles
    ]

    return jsonify(author_data), 200


@author_bp.route("/<int:author_id>", methods=["PUT"])
@admin_token_required
def update_author(current_admin, author_id):
    """Оновлює автора"""
    data = request.get_json()

    author_repo = get_author_repo()
    author = author_repo.get_by(id=author_id)
    if not author:
        raise ValueError("Автора не знайдено")

    update_data = {}
    updatable_fields = ["first_name", "last_name", "bio"]
    for field in updatable_fields:
        if field in data:
            if field in ["first_name", "last_name"] and not data.get(field):
                return jsonify({"msg": f"{field} не може бути порожнім"}), 400
            update_data[field] = data.get(field)

    updated_author = author_repo.update(author, update_data)
    return jsonify(updated_author.to_dict()), 200


@author_bp.route("/<int:author_id>", methods=["DELETE"])
@admin_token_required
def delete_author(current_admin, author_id):
    """Видаляє автора"""
    author_repo = get_author_repo()
    author = author_repo.get_by(id=author_id)
    if not author:
        raise ValueError("Автора не знайдено")

    article_repo = get_article_repo()
    author_articles = [
        article for article in article_repo.get_all() if article.author_id == author_id
    ]

    if author_articles:
        return (
            jsonify(
                {
                    "msg": "Неможливо видалити автора, оскільки у нього є статті",
                    "articles_count": len(author_articles),
                }
            ),
            400,
        )

    author_repo.delete(author)
    return jsonify({"msg": "Автора видалено"}), 200


@author_bp.route("/<int:author_id>/articles", methods=["GET"])
@admin_token_required
def get_author_articles(current_admin, author_id):
    """Отримує всі статті автора"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    status = request.args.get("status")

    author_repo = get_author_repo()
    author = author_repo.get_by(id=author_id)
    if not author:
        raise ValueError("Автора не знайдено")

    article_repo = get_article_repo()
    db_filters = {"author_id": author_id}
    if status:
        db_filters["status"] = status

    author_articles = article_repo.get_all_by(**db_filters)

    if status:
        author_articles = [
            article for article in author_articles if article.status == status
        ]

    author_articles = sorted(
        author_articles, key=lambda x: x.created_at or "", reverse=True
    )

    start = (page - 1) * per_page
    end = start + per_page
    paginated_articles = author_articles[start:end]

    result = [article.to_dict() for article in paginated_articles]

    return (
        jsonify(
            {
                "articles": result,
                "author": author.to_dict(),
                "page": page,
                "per_page": per_page,
                "total": len(author_articles),
                "status_filter": status,
            }
        ),
        200,
    )


@author_bp.route("/<int:author_id>/statistics", methods=["GET"])
@admin_token_required
def get_author_statistics(current_admin, author_id):
    """Отримує детальну статистику автора"""
    author_repo = get_author_repo()
    author = author_repo.get_by(id=author_id)
    if not author:
        raise ValueError("Автора не знайдено")

    article_repo = get_article_repo()
    author_articles = [
        article for article in article_repo.get_all() if article.author_id == author_id
    ]

    stats = {
        "author": author.to_dict(),
        "articles": {
            "total": len(author_articles),
            "by_status": {
                "published": len(
                    [a for a in author_articles if a.status == "published"]
                ),
                "draft": len([a for a in author_articles if a.status == "draft"]),
                "archived": len([a for a in author_articles if a.status == "archived"]),
            },
            "special": {
                "exclusive": len([a for a in author_articles if a.is_exclusive]),
                "breaking": len([a for a in author_articles if a.is_breaking]),
            },
        },
        "engagement": {
            "total_views": sum([a.views_count for a in author_articles]),
            "average_views": (
                round(
                    sum([a.views_count for a in author_articles])
                    / len(author_articles),
                    2,
                )
                if author_articles
                else 0
            ),
            "most_viewed_article": None,
        },
    }

    if author_articles:
        most_viewed = max(author_articles, key=lambda x: x.views_count)
        stats["engagement"]["most_viewed_article"] = {
            "id": most_viewed.id,
            "title": most_viewed.title,
            "views_count": most_viewed.views_count,
            "created_at": (
                most_viewed.created_at.isoformat() if most_viewed.created_at else None
            ),
        }

    category_stats = {}
    for article in author_articles:
        if article.category_id:
            if article.category_id not in category_stats:
                category_stats[article.category_id] = {"count": 0, "total_views": 0}
            category_stats[article.category_id]["count"] += 1
            category_stats[article.category_id]["total_views"] += article.views_count

    stats["categories"] = category_stats

    return jsonify(stats), 200


@author_bp.route("/search", methods=["GET"])
@admin_token_required
def search_authors(current_admin):
    """Пошук авторів за ім'ям, прізвищем або біографією"""
    query = request.args.get("q", "")
    limit = request.args.get("limit", 10, type=int)

    if not query:
        return jsonify({"msg": "Пошуковий запит є обов'язковим"}), 400

    author_repo = get_author_repo()
    authors = author_repo.get_all()

    query_lower = query.lower()
    found_authors = []

    for author in authors:
        match_score = 0
        author_data = author.to_dict()

        if query_lower in author.first_name.lower():
            match_score += 3
        if query_lower in author.last_name.lower():
            match_score += 3
        if author.bio and query_lower in author.bio.lower():
            match_score += 1

        if match_score > 0:
            author_data["match_score"] = match_score
            found_authors.append(author_data)

    found_authors = sorted(found_authors, key=lambda x: x["match_score"], reverse=True)
    found_authors = found_authors[:limit]

    return (
        jsonify(
            {
                "authors": found_authors,
                "query": query,
                "total_found": len(found_authors),
            }
        ),
        200,
    )
