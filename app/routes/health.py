from flask import Blueprint, jsonify, session

from app.utils.db_setup import ensure_mediumblob


health_bp = Blueprint('health', __name__)

@health_bp.route('/health')
def health_check():
    try:
        session['dummy'] = 'init'
        ensure_mediumblob()
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

    return jsonify({'status': 'ok'}), 200
