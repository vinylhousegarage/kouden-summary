from flask import Flask
from .config import Config
from .db import db, init_db
from .routes.main import main_bp
from . import models
from app.routes.health import health_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db(app)
    app.register_blueprint(main_bp)
    app.register_blueprint(health_bp)
    return app
