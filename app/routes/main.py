from flask import Flask
from app.config import Config
from app.routes.auth import auth_bp
from app.routes.dashboard import dashboard_bp

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
