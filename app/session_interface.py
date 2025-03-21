from flask_session import Session
from app.utils.encrypted_serializer import EncryptedSessionSerializer
from cryptography.fernet import Fernet
from app.config import Config

class CustomSession(Session):
    def __init__(self, app=None):
        super().__init__(app)
        self.serializer = EncryptedSessionSerializer(Fernet(Config.FERNET_KEY))
