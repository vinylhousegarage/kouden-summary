import requests
import urllib
from flask import current_app
from app.config import Config

def generate_cognito_login_url():
    encoded_scope = urllib.parse.quote(Config.COGNITO_SCOPE)

    return (
        f"{Config.COGNITO_DOMAIN}/login?"
        f"client_id={Config.COGNITO_CLIENT_ID}&"
        f"response_type=code&"
        f"scope={encoded_scope}&"
        f"redirect_uri={Config.COGNITO_REDIRECT_URI}"
    )

def send_cognito_token_request(grant_type, extra_data):
    url = f"{Config.COGNITO_DOMAIN}/oauth2/token"

    data = {
        "grant_type": grant_type,
        "client_id": Config.COGNITO_CLIENT_ID,
        "client_secret": Config.COGNITO_CLIENT_SECRET,
    }
    data.update(extra_data)

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(url, data=data, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        current_app.logger.error(f"Failed to get token: {response.text}")
        return None
