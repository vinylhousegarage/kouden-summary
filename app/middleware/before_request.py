from flask import request, redirect
from app.extensions import cognito_auth
from app.config import Config

def require_login(app):
    @app.before_request
    def _require_login():
        public_routes = ["health.health_check"]
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
    cognito_login_url = (
        f"{Config.COGNITO_DOMAIN}/login?"
        f"client_id={Config.COGNITO_CLIENT_ID}&response_type=code&"
        f"scope=openid+email&redirect_uri={Config.COGNITO_REDIRECT_URI}"
    )
    return redirect(cognito_login_url)
