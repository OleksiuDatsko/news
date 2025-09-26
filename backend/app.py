from dotenv import load_dotenv
import os
from flask_migrate import Migrate
from database import IDatabaseConnection
from flask import Flask, current_app, g
from flask_jwt_extended import JWTManager
from di.container import configure_dependencies
from blueprints import auth_bp, content_bp, subscription_bp
from config import config

load_dotenv()


def create_app(config_name="default"):
    app = Flask(__name__)

    config_class = config.get(config_name, config["default"])
    app.config.from_object(config_class)

    @app.before_request
    def attach_container():
        g.container = current_app.container

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
    app.register_blueprint(content_bp, url_prefix="/content")
    app.register_blueprint(subscription_bp, url_prefix="/subscriptions")

    @app.route("/")
    def hello():
        return {"message": "News API is running!", "config": config_name}

    return app


if __name__ == "__main__":
    config_name = os.environ.get("FLASK_CONFIG", "default")
    app = create_app(config_name)
    app.run(host="0.0.0.0", port=5000)
