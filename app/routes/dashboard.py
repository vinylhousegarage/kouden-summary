from flask import Blueprint, session, redirect, render_template

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def dashboard():
    if "access_token" not in session:
        return redirect("/login")

    return render_template("dashboard.html")
