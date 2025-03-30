from flask import Blueprint, current_app, request, session
from jose import jwt

from app.services.auth_service import exchange_code_for_token
from app.utils.auth_helpers import (redirect_to_cognito_login,
                                    redirect_to_login, redirect_to_root)
from app.utils.jwt_helpers import decode_cognito_jwt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    if 'access_token' in session:
        return redirect_to_root()

    return redirect_to_cognito_login()

@auth_bp.route('/oauth2/idpresponse')
def callback():
    code = request.args.get('code')
    error = request.args.get('error')
    error_description = request.args.get('error_description')

    if error:
        current_app.logger.error(f'❌ Cognitoからエラーが返されました: error={error}, description={error_description}')
        return redirect_to_login()

    if not code:
        current_app.logger.warning('⚠️ code が取得できませんでした')
        return redirect_to_login()

    try:
        tokens = exchange_code_for_token(code)

        access_token = tokens.get('access_token')
        id_token = tokens.get('id_token')
        refresh_token = tokens.get('refresh_token')

        session['access_token'] = access_token
        session['id_token'] = id_token
        session['refresh_token'] = refresh_token

        claims = decode_cognito_jwt(id_token, access_token)
        user_cognito_id = claims.get('sub')

        session['user_cognito_id'] = user_cognito_id
        return redirect_to_root()

    except jwt.ExpiredSignatureError:
        current_app.logger.warning('⚠️ トークンの有効期限が切れています')
        return redirect_to_login()

    except jwt.JWTClaimsError:
        current_app.logger.exception('❌ トークンのクレームが不正')
        return redirect_to_login()

    except AttributeError:
        current_app.logger.exception('❌ 属性アクセスに失敗')
        return redirect_to_login()

    except Exception:
        current_app.logger.exception('❌ 例外発生')
        return redirect_to_login()

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect_to_login()
