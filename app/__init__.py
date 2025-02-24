from flask import Flask, session, redirect, url_for, request
from app.config import Config
from app.extensions import init_oauth
from app.db import init_db
from app.routes.main import main_bp
from app.routes.health import health_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY

    init_db(app)

    init_oauth(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(health_bp)

    @app.before_request
    def require_login():
        if request.endpoint in ["health.health", "main.login", "main.authorize"]:
            return
        if "user" not in session:
            return redirect(url_for("main.login"))

    return app
