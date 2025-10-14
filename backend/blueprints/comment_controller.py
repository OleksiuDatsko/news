from flask import Blueprint, request, jsonify
from middleware.auth_middleware import token_required, permission_required
from repositories import get_comment_repo, get_article_repo
from services.comment_service import CommentService

comment_bp = Blueprint("comment", __name__)

@comment_bp.route("/articles/<int:article_id>/comments", methods=["GET"])
def get_comments(article_id):
    """Отримує коментарі для статті"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    service = CommentService(get_comment_repo(), get_article_repo())

    try:
        comments = service.get_comments_for_article(article_id, page, per_page)
        return jsonify({"comments": comments}), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@comment_bp.route("/articles/<int:article_id>/comments", methods=["POST"])
@token_required
@permission_required("comment")
def create_comment(current_user, article_id):
    """Створює новий коментар"""
    data = request.get_json()
    text = data.get("text")

    if not text:
        return jsonify({"msg": "Текст коментаря є обов'язковим"}), 400

    service = CommentService(get_comment_repo(), get_article_repo())

    try:
        comment = service.create_comment(current_user.id, article_id, text)
        return jsonify(comment), 201
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400
    except Exception as e:
        return jsonify({"msg": str(e)}), 500
    
@comment_bp.route("/comments/<int:comment_id>", methods=["GET"])
@token_required
def get_comment_by_id(current_user, comment_id):
    """Отримує коментар за ID"""
    service = CommentService(get_comment_repo(), get_article_repo())

    try:
        comment = service.get_comment_by_id(comment_id)
        return jsonify(comment), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@comment_bp.route("/comments/<int:comment_id>", methods=["PUT"])
@token_required
def update_comment(current_user, comment_id):
    """Оновлює коментар"""
    data = request.get_json()
    text = data.get("text")

    if not text:
        return jsonify({"msg": "Текст коментаря є обов'язковим"}), 400

    service = CommentService(get_comment_repo(), get_article_repo())

    try:
        updated = service.update_comment(current_user.id, comment_id, text)
        return jsonify(updated), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404
    except PermissionError as e:
        return jsonify({"msg": str(e)}), 403
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@comment_bp.route("/comments/<int:comment_id>", methods=["DELETE"])
@token_required
def delete_comment(current_user, comment_id):
    """Видаляє коментар"""
    service = CommentService(get_comment_repo(), get_article_repo())

    try:
        result = service.delete_comment(current_user.id, comment_id, current_user.is_admin)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404
    except PermissionError as e:
        return jsonify({"msg": str(e)}), 403
    except Exception as e:
        return jsonify({"msg": str(e)}), 500