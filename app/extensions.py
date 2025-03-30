from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from app.config import Config
from app.utils.encrypted_serializer import EncryptedSessionSerializer

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
session = Session()
session.serializer = EncryptedSessionSerializer(Config.FERNET_KEY)
