from app.config import Config
from app.extensions import oauth

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
