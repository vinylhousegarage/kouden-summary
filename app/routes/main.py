from flask import Blueprint, session, render_template
from app.utils.auth_helpers import redirect_to_cognito_login

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def main():
    if "access_token" not in session:
        return redirect_to_cognito_login()

    return render_template("main.html")
