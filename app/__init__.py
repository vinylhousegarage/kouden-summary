from flask import Flask
from .config import Config
from .db import db, init_db
from .routes.main import main_bp
from . import models

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db(app)
    app.register_blueprint(main_bp)
    return app
