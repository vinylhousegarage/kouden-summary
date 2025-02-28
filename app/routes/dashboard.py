from flask import Blueprint, session, redirect, render_template

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    """ログイン済みユーザー用のダッシュボード"""
    if "access_token" not in session:
        return redirect("/")

    return render_template("dashboard.html")
