from flask import Blueprint, redirect, session, request
from app.services.auth_service import exchange_code_for_token
from app.config import Config

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login")
def login():
    if "access_token" in session:
        return redirect("/")

    cognito_login_url = (
        f"https://{Config.COGNITO_DOMAIN}/login?"
        f"client_id={Config.COGNITO_CLIENT_ID}&response_type=code&"
        f"scope=openid+profile+email&redirect_uri={Config.COGNITO_REDIRECT_URI}"
    )
    return redirect(cognito_login_url)

@auth_bp.route("/oauth2/idpresponse")
def callback():
    code = request.args.get("code")
    if not code:
        return redirect("/login")

    tokens = exchange_code_for_token(code)
    if tokens:
        session["access_token"] = tokens.get("access_token")
        session["id_token"] = tokens.get("id_token")
        session["refresh_token"] = tokens.get("refresh_token")
        return redirect("/")
    else:
        return redirect("/login")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
