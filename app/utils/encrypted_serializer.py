import base64
import json

from cryptography.fernet import Fernet
from flask import current_app


class EncryptedSessionSerializer:
    def __init__(self, key):
        self.cipher = Fernet(key)

    def dumps(self, data):
        json_data = json.dumps(data)
        encrypted_data = self.cipher.encrypt(json_data.encode())
        return base64.b64encode(encrypted_data)

    def loads(self, encrypted_data):
        try:
            decrypted_data = self.cipher.decrypt(base64.b64decode(encrypted_data))
            return json.loads(decrypted_data.decode())
        except Exception:
            current_app.logger.exception('❌ セッション復号エラー')
            return None

    encode = dumps
    decode = loads
