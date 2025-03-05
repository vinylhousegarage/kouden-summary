import os

class Config:
    DB_HOST = os.getenv("DB_HOST", "db")
    DB_USER = os.getenv("MYSQL_USER")
    DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
    DB_NAME = os.getenv("MYSQL_DATABASE")

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
    AWS_REGION = os.getenv("AWS_REGION", "ap-northeast-1")
    AWS_COGNITO_USER_POOL_ID = os.getenv("AWS_COGNITO_USER_POOL_ID")
    AWS_COGNITO_USER_POOL_CLIENT_ID = os.getenv("AWS_COGNITO_USER_POOL_CLIENT_ID")

    COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN")
    COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")
    COGNITO_CLIENT_SECRET = os.getenv("COGNITO_CLIENT_SECRET")
    COGNITO_AUTHORITY = os.getenv("COGNITO_AUTHORITY")
    COGNITO_METADATA_URL = os.getenv("COGNITO_METADATA_URL")
    COGNITO_SCOPE = os.getenv("COGNITO_SCOPE", "email openid")
    COGNITO_REDIRECT_URI = os.getenv("COGNITO_REDIRECT_URI")
