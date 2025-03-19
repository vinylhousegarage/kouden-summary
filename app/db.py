from app.extensions import db, migrate

def init_db(app):
    db.init_app(app)
