from flask import Flask, session, redirect, url_for, request
from app.config import Config
from app.extensions import oauth
from app.db import init_db
from app.routes.main import main_bp
from app.routes.health import health_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY

    init_db(app)

    oauth.init_app(app)
    oauth.register(
        name="oidc",
        client_id=Config.COGNITO_CLIENT_ID,
        client_secret=Config.COGNITO_CLIENT_SECRET,
        authority=Config.COGNITO_AUTHORITY,
        server_metadata_url=Config.COGNITO_METADATA_URL,
        client_kwargs={"scope": Config.COGNITO_SCOPE}
    )

    app.register_blueprint(main_bp)
    app.register_blueprint(health_bp)

    @app.before_request
    def require_login():
        if request.endpoint in ["health.health", "main.login", "main.authorize"]:
            return
        if "user" not in session:
            return redirect(url_for("main.login"))

    return app
