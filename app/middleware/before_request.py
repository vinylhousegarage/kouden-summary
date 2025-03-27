import logging
from flask import request, session
from app.extensions import cognito_auth
from app.utils.auth_helpers import redirect_to_cognito_login
from app.services.auth_service import refresh_access_token

logger = logging.getLogger(__name__)

def require_login(app):
    @app.before_request
    def _require_login():
        public_routes = ['health.health_check', 'auth.callback']

        if request.endpoint is None:
            logger.warning('⚠️ `request.endpoint` が `None` なのでリダイレクトしません')
            return

        if request.endpoint in public_routes:
            logger.debug('✅ `public_routes` に含まれているためリダイレクトしません')
            return

        token = session.get('access_token')
        refresh_token = session.get('refresh_token')

        if token:
            try:
                claims = cognito_auth.verify_access_token(token, leeway=10)
                request.user = claims
                logger.info('✅ sessionの `access_token` の検証成功！', exc_info=True)
                return

            except Exception as e:
                logger.error('❌ sessionの `access_token` 検証エラー', exc_info=True)

        if refresh_token:
            new_tokens = refresh_access_token(refresh_token)

            if new_tokens and 'access_token' in new_tokens:
                session['access_token'] = new_tokens['access_token']

                try:
                    claims = cognito_auth.verify_access_token(new_tokens['access_token'], leeway=10)
                    request.user = claims
                    logger.info('✅ refresh_token で更新した `access_token` の検証成功！', exc_info=True)
                    return

                except Exception as e:
                    logger.error(f'❌ refresh_token で更新した `access_token` も検証エラー', exc_info=True)

        logger.warning("❌ `session['access_token']` 無効により再ログイン", exc_info=True)
        return redirect_to_cognito_login()
