from flask import Blueprint, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from sqlalchemy import text
from app.db import db
from app.config import Config
from app import oauth

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    try:
        db.session.execute(text("SELECT 1"))
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
