import os

from datetime import timedelta


class Config:
    DB_HOST = os.getenv('DB_HOST', 'db')
    DB_USER = os.getenv('MYSQL_USER')
    DB_PASSWORD = os.getenv('MYSQL_PASSWORD')
    DB_NAME = os.getenv('MYSQL_DATABASE')

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')

    AWS_REGION = os.getenv('AWS_REGION', 'ap-northeast-1')

    AWS_COGNITO_USER_POOL_ID = os.getenv('AWS_COGNITO_USER_POOL_ID')
    AWS_COGNITO_USER_POOL_CLIENT_ID = os.getenv('AWS_COGNITO_USER_POOL_CLIENT_ID')
    AWS_COGNITO_CLIENT_SECRET = os.getenv('AWS_COGNITO_CLIENT_SECRET')
    AWS_COGNITO_DOMAIN = os.getenv('AWS_COGNITO_DOMAIN')
    AWS_COGNITO_AUTHORITY = os.getenv('AWS_COGNITO_AUTHORITY')
    AWS_COGNITO_METADATA_URL = os.getenv('AWS_COGNITO_METADATA_URL')
    AWS_COGNITO_SCOPE = os.getenv('AWS_COGNITO_SCOPE', 'openid email profile')
    AWS_COGNITO_REDIRECT_URI = os.getenv('AWS_COGNITO_REDIRECT_URI')
    AWS_COGNITO_LOGOUT_URI = os.getenv('AWS_COGNITO_LOGOUT_URI')

    SESSION_TYPE = 'sqlalchemy'
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_USE_SIGNER = True
    SESSION_SQLALCHEMY_TABLE = 'sessions'
    SESSION_CLEANUP_N_REQUESTS = 100
    SESSION_SERIALIZER = 'app.utils.encrypted_serializer.EncryptedSessionSerializer'

    FERNET_KEY = os.getenv('FERNET_KEY')
