from flask import Blueprint, jsonify

content_bp = Blueprint('content', __name__)

@content_bp.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Content blueprint works!'})
