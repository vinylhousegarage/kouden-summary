from flask import Flask, session, redirect, url_for, request
from .config import Config
from .db import db, init_db
from .routes.main import main_bp
from .routes.health import health_bp
from authlib.integrations.flask_client import OAuth

oauth = OAuth()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.secret_key = config.SECRET_KEY

    init_db(app)

    oauth.init_app(app)
    oauth.register(
        name="oidc",
        client_id=config.COGNITO_CLIENT_ID,
        client_secret=config.COGNITO_CLIENT_SECRET,
        authority=config.COGNITO_AUTHORITY,
        server_metadata_url=config.COGNITO_METADATA_URL,
        client_kwargs={"scope": config.COGNITO_SCOPE}
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
