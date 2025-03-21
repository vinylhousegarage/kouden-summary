from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_cognito_lib import CognitoAuth
from authlib.integrations.flask_client import OAuth
from flask_session import Session
from app.utils.encrypted_serializer import EncryptedSessionSerializer
from cryptography.fernet import Fernet
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
cognito_auth = CognitoAuth()
oauth = OAuth()
session = Session()
session.serializer = EncryptedSessionSerializer(Fernet(Config.FERNET_KEY))
