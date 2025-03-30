from flask import current_app, request, session

from app.services.auth_service import refresh_access_token
from app.utils.auth_helpers import redirect_to_cognito_login
from app.utils.jwt_helpers import verify_cognito_jwt


def require_login(app):
    @app.before_request
    def _require_login():
        public_routes = ['health.health_check', 'auth.callback']

        if request.endpoint is None:
            current_app.logger.warning('⚠️ `request.endpoint` が `None` なのでリダイレクトしません')
            return

        if request.endpoint in public_routes:
            current_app.logger.info('✅ `public_routes` に含まれているためリダイレクトしません')
            return

        token = session.get('access_token')
        refresh_token = session.get('refresh_token')

        if token:
            try:
                claims = verify_cognito_jwt(token, leeway=10)
                request.user = claims
                return

            except Exception:
                current_app.logger.exception('❌ sessionの `access_token` 検証エラー')

        if refresh_token:
            new_tokens = refresh_access_token(refresh_token)

            if new_tokens and 'access_token' in new_tokens:
                session['access_token'] = new_tokens['access_token']

                try:
                    claims = verify_cognito_jwt(new_tokens['access_token'], leeway=10)
                    request.user = claims
                    return

                except Exception:
                    current_app.logger.exception('❌ refresh_token で更新した `access_token` も検証エラー')

        current_app.logger.warning("⚠️ `session['access_token']` 無効により再ログイン")
        return redirect_to_cognito_login()
