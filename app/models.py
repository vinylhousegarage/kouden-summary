from app.extensions import db

class Summary(db.Model):
    __tablename__ = "summaries"

    id = db.Column(db.Integer, primary_key=True)
    giver_name = db.Column(db.String(100), nullable=False, info={"label": "氏名"})
    amount = db.Column(db.Integer, nullable=False, info={"label": "金額"})
    address = db.Column(db.String(250), info={"label": "住所"})
    tel = db.Column(db.String(20), info={"label": "電話"})
    note = db.Column(db.String(250), info={"label": "備考"})
    user_cognito_id = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)
