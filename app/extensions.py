from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cognito_lib import CognitoAuth
from authlib.integrations.flask_client import OAuth
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
cognito_auth = CognitoAuth()
oauth = OAuth()
