from flask import Flask
from app.routes.auth import auth_bp
from app.routes.dashboard import dashboard_bp

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)

if __name__ == "__main__":
    app.run(debug=True)
