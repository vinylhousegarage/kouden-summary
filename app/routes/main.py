from flask import Blueprint, session, redirect, render_template

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def main():
    if "access_token" not in session:
        return redirect("/login")

    return render_template("main.html")
