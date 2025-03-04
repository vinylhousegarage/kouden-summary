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
            return redirect("/")
        else:
            return redirect("/login")

    except AttributeError:
            return redirect("/login")
    except Exception:
            return redirect("/login")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
