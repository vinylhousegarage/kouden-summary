from flask import Flask
from .config import Config
from .db import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    @app.route("/")
    def index():
        try:
            db.session.execute("SELECT 1")
            return "Database connection successful!"
        except Exception as e:
            return f"Database connection failed: {str(e)}", 500

    return app
