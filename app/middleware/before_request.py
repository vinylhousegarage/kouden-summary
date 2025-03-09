import sys
from flask import request, session
from app.extensions import cognito_auth
from app.utils.auth_helpers import redirect_to_cognito_login

def require_login(app):
    @app.before_request
    def _require_login():
        print(f"📌 `request.endpoint`: {request.endpoint}", file=sys.stderr, flush=True)

        public_routes = ["health.health_check", "auth.callback"]

        if request.endpoint is None:
            print("⚠️ `request.endpoint` が `None` なのでリダイレクトしません", file=sys.stderr, flush=True)
            return

        if request.endpoint in public_routes:
            print("✅ `public_routes` に含まれているためリダイレクトしません", file=sys.stderr, flush=True)
            return

        token = session.get("access_token")
        if token:
            print("✅ セッションから `access_token` を取得", file=sys.stderr, flush=True)
            try:
                claims = cognito_auth.verify_access_token(token, leeway=10)
                request.user = claims
                print("✅ トークン検証成功！", file=sys.stderr, flush=True)
                return
            except Exception as e:
                print(f"❌ セッションの `access_token` 検証エラー: {e}", file=sys.stderr, flush=True)

        print("❌ `session['access_token']` が無効または存在しないのでリダイレクトします", file=sys.stderr, flush=True)
        return redirect_to_cognito_login()
