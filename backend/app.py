from dotenv import load_dotenv
import os
from flask_cors import CORS
from flask_migrate import Migrate
from database import IDatabaseConnection
from flask import Flask, current_app, g
from flask_jwt_extended import JWTManager
from di.container import configure_dependencies
from blueprints import (
    auth_bp,
    subscription_bp,
    article_bp,
    admin_bp,
    ad_bp,
    comment_bp,
    category_bp,
    notification_bp
)
from config import config

load_dotenv()


def create_app(config_name="default"):
    app = Flask(__name__)
    CORS(app, origins="*", supports_credentials=True)

    config_class = config.get(config_name, config["default"])
    app.config.from_object(config_class)
    app.config["SQLALCHEMY_ECHO"] = False
    
    @app.before_request
    def attach_services():
        """
        Виконується перед кожним запитом.
        Створює ОДНУ сесію на весь запит і зберігає її в 'g'.
        """
        g.container = current_app.container
        db_connection = g.container.resolve(IDatabaseConnection)
        g.db_session = db_connection.get_session()

    @app.teardown_request
    def teardown_session(exception=None):
        """
        Виконується після кожного запиту.
        Закриває сесію і повертає з'єднання в пул.
        """
        db_session = g.pop('db_session', None)
        if db_session is not None:
            db_session.close()

    jwt = JWTManager()
    jwt.init_app(app)

    try:
        container = configure_dependencies(app.config)
        app.container = container
    except Exception as e:
        print(f"Error configuring dependencies: {e}")
        raise

    Migrate(app, container.resolve(IDatabaseConnection))

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(subscription_bp, url_prefix="/subscriptions")
    app.register_blueprint(article_bp, url_prefix="/articles")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(ad_bp, url_prefix="/ads")
    app.register_blueprint(comment_bp, url_prefix="/")
    app.register_blueprint(category_bp, url_prefix="/categories")
    app.register_blueprint(notification_bp, url_prefix="/notifications")
    
    @app.route("/")
    def hello():
        return {"message": "News API is running!", "config": config_name}

    return app


if __name__ == "__main__":
    config_name = os.environ.get("FLASK_CONFIG", "default")
    app = create_app(config_name)
    app.run(host="0.0.0.0", port=5000, threaded=True)
