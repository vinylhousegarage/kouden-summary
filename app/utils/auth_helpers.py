import requests
from flask import current_app, redirect

from app.config import Config


def redirect_to_root():
    return redirect('/')

def redirect_to_login():
    return redirect('/login')

def generate_cognito_url(endpoint, params):
    base_url = f'https://{Config.AWS_COGNITO_DOMAIN}/{endpoint}'
    query = '&'.join(f'{key}={value}' for key, value in params.items())
    return f'{base_url}?{query}'

def generate_cognito_login_url():
    return generate_cognito_url('login', {
        'client_id': Config.AWS_COGNITO_USER_POOL_CLIENT_ID,
        'response_type': 'code',
        'scope': Config.AWS_COGNITO_SCOPE,
        'redirect_uri': Config.AWS_COGNITO_REDIRECT_URI,
    })

def generate_cognito_logout_url():
    return generate_cognito_url('logout', {
        'client_id': Config.AWS_COGNITO_USER_POOL_CLIENT_ID,
        'logout_uri': Config.AWS_COGNITO_REDIRECT_URI,
    })

def redirect_to_cognito_login():
    return redirect(generate_cognito_login_url())

def send_cognito_token_request(grant_type, extra_data):
    url = f'{Config.AWS_COGNITO_DOMAIN}/oauth2/token'

    data = {
        'grant_type': grant_type,
        'client_id': Config.AWS_COGNITO_USER_POOL_CLIENT_ID,
        'client_secret': Config.AWS_COGNITO_CLIENT_SECRET,
    }
    data.update(extra_data)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=data, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        current_app.logger.error(f'Failed to get token: {response.text}')
        return None
