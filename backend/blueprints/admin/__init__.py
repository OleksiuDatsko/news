from flask import Blueprint
from .auth_controller import auth_bp

admin_bp = Blueprint('admin', __name__)
admin_bp.register_blueprint(auth_bp, url_prefix='/auth', name='admin_auth')
