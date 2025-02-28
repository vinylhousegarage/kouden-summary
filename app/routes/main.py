from flask import Blueprint, redirect, url_for, session
from app.extensions import db, oauth
from app.models import Summary

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def index():
    try:
        db.session.query(Summary).first()
        return "Database connection successful!"
    except Exception as e:
        return f"Database connection failed: {str(e)}", 500
