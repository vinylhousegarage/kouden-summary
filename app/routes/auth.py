from flask import Blueprint, session, request
from app.services.auth_service import exchange_code_for_token
from app.utils.auth_helpers import redirect_to_root, redirect_to_login, redirect_to_cognito_login

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login")
def login():
    if "access_token" in session:
        return redirect_to_root()

    return redirect_to_cognito_login()

@auth_bp.route("/oauth2/idpresponse")
def callback():
    try:
        code = request.args.get("code")
        print(f"📌 受け取ったコード: {code}")  # 🔹 `code` が正しく取得できているかログ出力

        if not code:
            print("❌ `code` が取得できませんでした！ログインページへリダイレクトします。")
            return redirect_to_login()

        print(f"🔄 `exchange_code_for_token()` を実行します。code={code}")  # 🔹 トークン取得の直前にログ
        tokens = exchange_code_for_token(code)

        if tokens:
            session["access_token"] = tokens.get("access_token")
            session["id_token"] = tokens.get("id_token")
            session["refresh_token"] = tokens.get("refresh_token")
            print(f"✅ トークン取得成功！tokens={tokens}")  # 🔹 トークン取得成功時のログ
            return redirect_to_root()
        else:
            print(f"❌ トークン取得失敗！code={code}")  # 🔹 失敗した場合のログ
            return redirect_to_login()

    except AttributeError as e:
        print(f"❌ AttributeError: {e}")  # 🔹 `AttributeError` の詳細ログ
        return redirect_to_login()
    except Exception as e:
        print(f"❌ 例外発生: {e}")  # 🔹 その他の例外のログ
        return redirect_to_login()

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect_to_login()
