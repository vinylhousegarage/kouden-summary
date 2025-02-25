from flask import session, redirect, url_for, request

def require_login(app):
    @app.before_request
    def _require_login():
        if request.endpoint in ["health.health_check", "main.login", "main.authorize"]:
            return

        if "user" not in session:
            return redirect(url_for("main.login"))
