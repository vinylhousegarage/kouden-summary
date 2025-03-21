import sys
from flask import Blueprint, session, request
from jose import jwt
from app.services.auth_service import exchange_code_for_token
from app.utils.auth_helpers import redirect_to_root, redirect_to_login, redirect_to_cognito_login

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    if 'access_token' in session:
        return redirect_to_root()

    return redirect_to_cognito_login()

@auth_bp.route('/oauth2/idpresponse')
def callback():
    try:
        code = request.args.get('code')
        print(f'📌 受け取ったコード: {code}', file=sys.stderr, flush=True)

        if not code:
            print('❌ `code` が取得できませんでした！ログインページへリダイレクトします。', file=sys.stderr, flush=True)
            return redirect_to_login()

        print(f'🔄 `exchange_code_for_token()` を実行します。code={code}', file=sys.stderr, flush=True)
        tokens = exchange_code_for_token(code)

        if tokens:
            access_token = tokens.get('access_token')
            id_token = tokens.get('id_token')
            refresh_token = tokens.get('refresh_token')

            print(f'✅ トークン取得成功！', file=sys.stderr, flush=True)
            print(f"  🔹 access_token: {'取得成功' if access_token else '取得失敗'}", file=sys.stderr, flush=True)
            print(f"  🔹 id_token: {'取得成功' if id_token else '取得失敗'}", file=sys.stderr, flush=True)
            print(f"  🔹 refresh_token: {'取得成功' if refresh_token else '取得失敗'}", file=sys.stderr, flush=True)

            session['access_token'] = access_token
            session['id_token'] = id_token
            session['refresh_token'] = refresh_token

            claims = jwt.get_unverified_claims(id_token)
            user_cognito_id = claims.get('sub')

            print(f"  🔹 user_cognito_id: {'取得成功' if user_cognito_id else '取得失敗'}", file=sys.stderr, flush=True)
            session['user_cognito_id'] = user_cognito_id

            return redirect_to_root()
        else:
            print(f'❌ トークン取得失敗！code={code}', file=sys.stderr, flush=True)
            return redirect_to_login()

    except AttributeError as e:
        print(f'❌ AttributeError: {e}', file=sys.stderr, flush=True)
        return redirect_to_login()
    except Exception as e:
        print(f'❌ 例外発生: {e}', file=sys.stderr, flush=True)
        return redirect_to_login()

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect_to_login()
