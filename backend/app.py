from dotenv import load_dotenv
import os

load_dotenv()

from flask import Flask
from flask_jwt_extended import JWTManager
from di.container import configure_dependencies
from blueprints.auth_controller import auth_bp
from blueprints.content_controller import content_bp
from config import config

def create_app(config_name='default'):
    app = Flask(__name__)
    
    config_class = config.get(config_name, config['default'])
    app.config.from_object(config_class)
    
    jwt = JWTManager()
    jwt.init_app(app)
    
    try:
        container = configure_dependencies(app.config)
        app.container = container
    except Exception as e:
        print(f"Error configuring dependencies: {e}")
        raise
    
    with app.app_context():
        from repositories.interfaces import IDatabaseConnection
        db_connection = container.resolve(IDatabaseConnection)
        db_connection.create_tables()
        print("Database tables created successfully!")
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(content_bp, url_prefix='/content')
    
    @app.route('/')
    def hello():
        return {'message': 'News API is running!', 'config': config_name}
    
    return app

if __name__ == '__main__':
    config_name = os.environ.get('FLASK_CONFIG', 'development')
    app = create_app(config_name)
    app.run(debug=True, host='0.0.0.0', port=5000)
