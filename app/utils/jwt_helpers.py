import logging
import requests
from flask import flash, redirect, url_for
from jose import jwt
from jose.utils import base64url_decode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from app.config import Config

logger = logging.getLogger(__name__)

def get_cognito_jwk():
    jwks_url = f'https://cognito-idp.{Config.AWS_REGION}.amazonaws.com/{Config.AWS_COGNITO_USER_POOL_ID}/.well-known/jwks.json'
    response = requests.get(jwks_url)
    return response.json()['keys']

def get_public_key_from_jwk(jwks, kid):
    key = next((k for k in jwks if k['kid'] == kid), None)

    if key is None:
        logger.warning(f'kid={kid} の公開鍵が見つかりませんでした')
        flash('ログイン状態が期限切れになっています')
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

def decode_cognito_jwt(id_token, access_token):
    jwks = get_cognito_jwk()
    headers = jwt.get_unverified_header(id_token)
    kid = headers['kid']
    pem_key = get_public_key_from_jwk(jwks, kid)

    claims = jwt.decode(
        id_token,
        pem_key,
        algorithms=['RS256'],
        audience=Config.AWS_COGNITO_USER_POOL_CLIENT_ID,
        access_token=access_token,
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
            options={'verify_exp': True},
            leeway=leeway
        )
        return claims

    except Exception:
        logger.exception('❌ access_token の検証に失敗しました')
        raise
