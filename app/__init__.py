from flask import Flask
from app.config import Config
from app.extensions import csrf, cognito_auth, migrate, db, session
from app.oauth import init_oauth
from app.routes.main import main_bp
from app.routes.health import health_bp
from app.routes.auth import auth_bp
from app.routes.summaries import summaries_bp
from app.middleware.before_request import require_login
from app.logging_config import check_existing_handlers, setup_logging
from app.middleware.request_logging import setup_request_logging
from app.utils.encrypted_serializer import EncryptedSessionSerializer

def create_app():
    from app.models import Summary

    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY

    check_existing_handlers(app)
    setup_logging(app)
    setup_request_logging(app)

    csrf.init_app(app)
    cognito_auth.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)

    app.config['SESSION_SQLALCHEMY'] = db
    session.init_app(app)
    app.session_interface.serializer = EncryptedSessionSerializer(Config.FERNET_KEY)

    init_oauth(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(summaries_bp)

    require_login(app)

    return app
