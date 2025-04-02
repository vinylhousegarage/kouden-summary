import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from flask import current_app, flash, redirect, session, url_for
from jose import jwt
from jose.utils import base64url_decode

from app.config import Config


def get_cognito_jwk():
    jwks_url = f'https://cognito-idp.{Config.AWS_REGION}.amazonaws.com/{Config.AWS_COGNITO_USER_POOL_ID}/.well-known/jwks.json'
    response = requests.get(jwks_url)
    return response.json()['keys']

def get_public_key_from_jwk(jwks, kid):
    key = next((k for k in jwks if k['kid'] == kid), None)

    if key is None:
        current_app.logger.warning(f'⚠️ kid={kid} 公開鍵取得失敗')
        flash('再ログインしてください')
        return redirect(url_for('auth.login'))

    n = base64url_decode(key['n'].encode('utf-8'))
    e = base64url_decode(key['e'].encode('utf-8'))

    public_key = rsa.RSAPublicNumbers(
        e=int.from_bytes(e, 'big'),
        n=int.from_bytes(n, 'big')
    ).public_key(default_backend())

    pem_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pem_key

def decode_cognito_jwt(id_token):
    jwks = get_cognito_jwk()
    headers = jwt.get_unverified_header(id_token)
    kid = headers['kid']
    pem_key = get_public_key_from_jwk(jwks, kid)

    claims = jwt.decode(
        id_token,
        pem_key,
        algorithms=['RS256'],
        audience=Config.AWS_COGNITO_USER_POOL_CLIENT_ID,
        issuer=f'https://cognito-idp.{Config.AWS_REGION}.amazonaws.com/{Config.AWS_COGNITO_USER_POOL_ID}'
    )
    return claims

def verify_cognito_jwt(access_token, leeway=10):
    try:
        jwks = get_cognito_jwk()
        headers = jwt.get_unverified_header(access_token)
        kid = headers['kid']
        pem_key = get_public_key_from_jwk(jwks, kid)
        claims = jwt.decode(
            access_token,
            pem_key,
            algorithms=['RS256'],
            audience=Config.AWS_COGNITO_USER_POOL_CLIENT_ID,
            issuer=f'https://cognito-idp.{Config.AWS_REGION}.amazonaws.com/{Config.AWS_COGNITO_USER_POOL_ID}',
            options={
                'verify_exp': True,
                'leeway': leeway,
            }
        )
        return claims

    except Exception:
        current_app.logger.exception('❌ access_token 検証失敗')

def validate_access_token(token):
    claims = verify_cognito_jwt(token)
    if claims:
        return claims
    current_app.logger.info('✅ 無効なトークンのためセッションをクリア')
    session.clear()
    return None
