from flask import session, redirect, url_for, request

def require_login(app):
    @app.before_request
    def _require_login():
        app.logger.debug(f"Before request - request.endpoint: {request.endpoint}")

        if request.endpoint in ["health.health", "main.login", "main.authorize"]:
            return

        if "user" not in session:
            return redirect(url_for("main.login"))
