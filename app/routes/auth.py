from flask import Blueprint
from app.extensions import cognito_auth

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/user')
def get_user():
    claims = cognito_auth.get_current_user_claims()
    if claims:
        return {
            "sub": claims.get("sub"),
            "email": claims.get("email"),
            "name": claims.get("name")
        }
    return {"error": "Unauthorized"}, 401
