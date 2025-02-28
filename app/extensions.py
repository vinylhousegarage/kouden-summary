from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cognito_lib import CognitoAuth
from authlib.integrations.flask_client import OAuth
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
cognito_auth = CognitoAuth()
oauth = OAuth()

def init_oauth(app):
    oauth.init_app(app)
    oauth.register(
        name="oidc",
        client_id=Config.COGNITO_CLIENT_ID,
        client_secret=Config.COGNITO_CLIENT_SECRET,
        authority=Config.COGNITO_AUTHORITY,
        server_metadata_url=Config.COGNITO_METADATA_URL,
        client_kwargs={"scope": Config.COGNITO_SCOPE}
    )
