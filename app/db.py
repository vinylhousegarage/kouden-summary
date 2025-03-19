from app.extensions import db

def init_db(app):
    db.init_app(app)
