from flask import request, redirect
from app.extensions import cognito_auth
from app.config import Config

def require_login(app):
    @app.before_request
    def _require_login():
        public_routes = ["health.health_check"]
        if request.endpoint in public_routes:
            return

        claims = cognito_auth.get_current_user_claims()
        if not claims:
            cognito_login_url = (
                f"https://{Config.COGNITO_DOMAIN}/login?"
                f"client_id={Config.COGNITO_CLIENT_ID}&response_type=code&"
                f"scope=openid+profile+email&redirect_uri={Config.COGNITO_REDIRECT_URI}"
            )
            return redirect(cognito_login_url)
