from flask import Blueprint
from app.db import db
from sqlalchemy import text

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    try:
        db.session.execute(text("SELECT 1"))
        return "Database connection successful!"
    except Exception as e:
        return f"Database connection failed: {str(e)}", 500
