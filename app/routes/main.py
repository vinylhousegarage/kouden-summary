from flask import Blueprint, session, redirect, render_template
from app.utils.auth_helpers import generate_cognito_login_url

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def main():
    if "access_token" not in session:
        return redirect(generate_cognito_login_url())

    return render_template("main.html")
