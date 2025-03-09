from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_cognito_lib import CognitoAuth
from authlib.integrations.flask_client import OAuth
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
cognito_auth = CognitoAuth()
oauth = OAuth()
