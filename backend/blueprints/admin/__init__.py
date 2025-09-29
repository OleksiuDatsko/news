from flask import Blueprint
from .auth_controller import auth_bp
from .subscription_controller import subscription_bp
from .category_controller import category_bp
from .article_controller import article_bp
from .user_controller import user_bp
from .author_controller import author_bp
from .ad_controller import ad_bp
from .admin_user_controller import admin_user_bp

admin_bp = Blueprint("admin", __name__)
admin_bp.register_blueprint(auth_bp, url_prefix="/auth", name="admin_auth")
admin_bp.register_blueprint(
    subscription_bp, url_prefix="/subscriptions", name="admin_subscriptions"
)
admin_bp.register_blueprint(
    category_bp, url_prefix="/categories", name="admin_categories"
)
admin_bp.register_blueprint(article_bp, url_prefix="/articles", name="admin_articles")
admin_bp.register_blueprint(user_bp, url_prefix="/users", name="admin_users")
admin_bp.register_blueprint(author_bp, url_prefix="/authors", name="admin_authors")
admin_bp.register_blueprint(ad_bp, url_prefix="/ads", name="admin_ads")
admin_bp.register_blueprint(
    admin_user_bp, url_prefix="/admin-users", name="admin_admin_users"
)
