import sys
from flask import request
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

        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        else:
            token = None

        if token:
            try:
                claims = cognito_auth.verify_access_token(token, leeway=10)
                request.user = claims
                print("✅ トークン検証成功！", file=sys.stderr, flush=True)
            except Exception as e:
                print(f"❌ トークン検証エラー: {e}", file=sys.stderr, flush=True)
                return redirect_to_cognito_login()
        else:
            print("❌ `Authorization` ヘッダーがないのでリダイレクトします", file=sys.stderr, flush=True)
            return redirect_to_cognito_login()
