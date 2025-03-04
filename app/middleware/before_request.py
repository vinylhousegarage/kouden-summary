from flask import request, redirect
from app.extensions import cognito_auth
from app.utils.auth_helpers import generate_cognito_login_url

def require_login(app):
    @app.before_request
    def _require_login():
        public_routes = ["health.health_check", "auth.callback"]
        if request.endpoint in public_routes:
            return

        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        else:
            token = None

        if token:
            try:
                claims = cognito_auth.verify_access_token(token, leeway=10)
                request.user = claims
            except Exception:
                return redirect_to_login()
        else:
            return redirect_to_login()

def redirect_to_login():
    return redirect(generate_cognito_login_url())
