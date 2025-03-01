from app.config import Config

def generate_cognito_login_url():
    return (
        f"{Config.COGNITO_DOMAIN}/login?"
        f"client_id={Config.COGNITO_CLIENT_ID}&response_type=code&"
        f"scope=openid+email&redirect_uri={Config.COGNITO_REDIRECT_URI}"
    )
