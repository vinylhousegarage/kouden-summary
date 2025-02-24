from flask import Blueprint, redirect, url_for, session
from app.extensions import db, oauth
from app.models import User

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def index():
    try:
        db.session.query(User).first()
        return "Database connection successful!"
    except Exception as e:
        return f"Database connection failed: {str(e)}", 500

@main_bp.route('/login')
def login():
    return oauth.oidc.authorize_redirect(url_for("main.authorize", _external=True))

@main_bp.route('/authorize')
def authorize():
    token = oauth.oidc.authorize_access_token()
    user = token.get("userinfo")
    session["user"] = user
    return redirect(url_for("main.index"))

@main_bp.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("main.index"))
