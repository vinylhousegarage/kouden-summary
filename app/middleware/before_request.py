import sys
from flask import request, session
from app.extensions import cognito_auth
from app.utils.auth_helpers import redirect_to_cognito_login
from app.services.auth_service import refresh_access_token

def require_login(app):
    @app.before_request
    def _require_login():
        print(f'📌 `request.endpoint`: {request.endpoint}', file=sys.stderr, flush=True)

        public_routes = ['health.health_check', 'auth.callback']

        if request.endpoint is None:
            print('⚠️ `request.endpoint` が `None` なのでリダイレクトしません', file=sys.stderr, flush=True)
            return

        if request.endpoint in public_routes:
            print('✅ `public_routes` に含まれているためリダイレクトしません', file=sys.stderr, flush=True)
            return

        token = session.get('access_token')
        refresh_token = session.get('refresh_token')

        if token:
            print('✅ セッションから `access_token` を取得', file=sys.stderr, flush=True)
            try:
                claims = cognito_auth.verify_access_token(token, leeway=10)
                request.user = claims
                print('✅ トークン検証成功！', file=sys.stderr, flush=True)
                return
            except Exception as e:
                print(f'❌ セッションの `access_token` 検証エラー: {e}', file=sys.stderr, flush=True)

        if refresh_token:
            print('🔄 `refresh_access_token()` を実行してトークンを更新します', file=sys.stderr, flush=True)
            new_tokens = refresh_access_token(refresh_token)

            if new_tokens and 'access_token' in new_tokens:
                session['access_token'] = new_tokens['access_token']
                print('✅ `access_token` を更新しました', file=sys.stderr, flush=True)

                try:
                    claims = cognito_auth.verify_access_token(new_tokens['access_token'], leeway=10)
                    request.user = claims
                    print('✅ 更新した `access_token` の検証成功！', file=sys.stderr, flush=True)
                    return
                except Exception as e:
                    print(f'❌ 更新した `access_token` も検証エラー: {e}', file=sys.stderr, flush=True)

        print("❌ `session['access_token']` が無効で、更新もできなかったのでログインを求めます", file=sys.stderr, flush=True)
        return redirect_to_cognito_login()
