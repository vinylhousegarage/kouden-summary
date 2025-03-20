from flask import Blueprint, session, jsonify

health_bp = Blueprint('health', __name__)

@health_bp.route('/health')
def health_check():
    try:
        session['dummy'] = 'init'
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

    return jsonify({'status': 'ok'}), 200
