from app.extensions import db

class Summary(db.Model):
    __tablename__ = 'summaries'
    id = db.Column(db.Integer, primary_key=True)
    giver_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(250), nullable=True)
    tel = db.Column(db.String(15), nullable=True)
    note = db.Column(db.String(250), nullable=True)
    user_cognito_id = db.Column(db.String(50), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
