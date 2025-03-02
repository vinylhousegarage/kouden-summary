from flask import Blueprint, redirect, session, request
from app.services.auth_service import exchange_code_for_token
from app.utils.auth_helpers import generate_cognito_login_url

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login")
def login():
    if "access_token" in session:
        return redirect("/")

    return redirect(generate_cognito_login_url())

@auth_bp.route("/oauth2/idpresponse")
def callback():
    print("🚀 callback() が実行された")  # コンテナの標準出力に表示
    current_app.logger.info("🚀 callback() が実行された")

    try:
        code = request.args.get("code")
        if not code:
            current_app.logger.error("❌ 認可コードが見つかりません")
            return redirect("/login")

        current_app.logger.info(f"✅ 取得した認可コード: {code}")

        tokens = exchange_code_for_token(code)

        if tokens:
            session["access_token"] = tokens.get("access_token")
            session["id_token"] = tokens.get("id_token")
            session["refresh_token"] = tokens.get("refresh_token")
            current_app.logger.info("✅ トークンの取得に成功しました")
            return redirect("/")
        else:
            current_app.logger.error("❌ トークン取得失敗！ (401 Unauthorized)")
            return redirect("/login")

    except AttributeError as e:
        current_app.logger.error(f"❌ `tokens` が `None` だったため、エラー発生: {str(e)}")
        return redirect("/login")

    except Exception as e:
        current_app.logger.error(f"❌ 予期しないエラー発生: {str(e)}")
        return redirect("/login")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
