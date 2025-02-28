import requests
from flask import current_app
from app.config import Config

def exchange_code_for_token(code):
    url = f"https://{Config.COGNITO_DOMAIN}/oauth2/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": Config.COGNITO_CLIENT_ID,
        "client_secret": Config.COGNITO_CLIENT_SECRET,
        "code": code,
        "redirect_uri": Config.COGNITO_REDIRECT_URI
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        current_app.logger.error(f"Failed to exchange code: {response.text}")
        return None

def refresh_access_token(refresh_token):
    url = f"https://{Config.COGNITO_DOMAIN}/oauth2/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": Config.COGNITO_CLIENT_ID,
        "client_secret": Config.COGNITO_CLIENT_SECRET,
        "refresh_token": refresh_token
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        current_app.logger.error(f"Failed to refresh token: {response.text}")
        return None
