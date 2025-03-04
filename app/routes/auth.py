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
        if not code:
            return redirect_to_login

        tokens = exchange_code_for_token(code)

        if tokens:
            session["access_token"] = tokens.get("access_token")
            session["id_token"] = tokens.get("id_token")
            session["refresh_token"] = tokens.get("refresh_token")
            return redirect_to_root()
        else:
            return redirect_to_login()

    except AttributeError:
            return redirect_to_login()
    except Exception:
            return redirect_to_login()

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect_to_login()
