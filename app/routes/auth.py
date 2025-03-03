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
    try:
        code = request.args.get("code")
        if not code:
            return redirect("/login")

        tokens = exchange_code_for_token(code)

        if tokens:
            session["access_token"] = tokens.get("access_token")
            session["id_token"] = tokens.get("id_token")
            session["refresh_token"] = tokens.get("refresh_token")

            response = make_response("ログイン成功！リダイレクトします", 302)
            response.headers["Location"] = "/"
        else:
            response = make_response("ログイン失敗", 302)
            response.headers["Location"] = "/login"

    except AttributeError as e:
        response = make_response("エラーが発生しました", 302)
        response.headers["Location"] = "/login"

    except Exception as e:
        response = make_response("サーバーエラー", 302)
        response.headers["Location"] = "/login"

    return response

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
