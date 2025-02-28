from flask import request, jsonify
from app.extensions import cognito_auth

def require_login(app):
    @app.before_request
    def _require_login():
        public_routes = ["health.health_check", "auth.get_user"]
        if request.endpoint in public_routes:
            return

        claims = cognito_auth.get_current_user_claims()
        if not claims:
            return jsonify({"error": "Unauthorized"}), 401
