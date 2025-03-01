from app.config import Config
from app.utils.auth_helpers import send_cognito_token_request

def exchange_code_for_token(code):
    return send_cognito_token_request("authorization_code", {"code": code, "redirect_uri": Config.COGNITO_REDIRECT_URI})

def refresh_access_token(refresh_token):
    return send_cognito_token_request("refresh_token", {"refresh_token": refresh_token})
