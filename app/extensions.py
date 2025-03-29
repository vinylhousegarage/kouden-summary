from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from authlib.integrations.flask_client import OAuth
from flask_session import Session
from app.utils.encrypted_serializer import EncryptedSessionSerializer
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
oauth = OAuth()
session = Session()
session.serializer = EncryptedSessionSerializer(Config.FERNET_KEY)
