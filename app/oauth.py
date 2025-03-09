from app.config import Config
from app.extensions import oauth

def init_oauth(app):
    oauth.init_app(app)
    oauth.register(
        name="oidc",
        client_id=Config.AWS_COGNITO_USER_POOL_CLIENT_ID,
        client_secret=Config.AWS_COGNITO_CLIENT_SECRET,
        authority=Config.AWS_COGNITO_AUTHORITY,
        server_metadata_url=Config.AWS_COGNITO_METADATA_URL,
        client_kwargs={"scope": Config.AWS_COGNITO_SCOPE}
    )
