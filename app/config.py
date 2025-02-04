import os

class Config:
    DB_HOST = os.getenv("DB_HOST", "db")
    DB_USER = os.getenv("MYSQL_USER")
    DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
    DB_NAME = os.getenv("MYSQL_DATABASE")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
