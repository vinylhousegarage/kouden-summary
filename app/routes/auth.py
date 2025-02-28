from flask import Blueprint, redirect, session, request, jsonify
from app.services.auth_service import exchange_code_for_token
from app.config import Config

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/oauth2/idpresponse")
def callback():
    """Cognito からのリダイレクト後、トークンを取得"""
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "No authorization code received"}), 400

    tokens = exchange_code_for_token(code)
    if tokens:
        session["access_token"] = tokens.get("access_token")
        session["id_token"] = tokens.get("id_token")
        session["refresh_token"] = tokens.get("refresh_token")  # ここで refresh_token も保存
        return redirect("/dashboard")
    else:
        return jsonify({"error": "Token exchange failed"}), 400
