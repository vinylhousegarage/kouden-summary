from flask import Flask
from flask_wtf import CSRFProtect
from app.config import Config
from app.extensions import init_oauth
from app.db import init_db
from app.routes.main import main_bp
from app.routes.health import health_bp
from app.middleware.before_request import require_login
from app.logging_config import setup_logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY

    CSRFProtect(app)
    setup_logging(app)
    init_db(app)
    init_oauth(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(health_bp)

    require_login(app)

    return app
