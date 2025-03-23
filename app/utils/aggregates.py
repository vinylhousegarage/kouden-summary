from sqlalchemy import func
from app.extensions import db
from app.models import Summary

def calculate_totals():
    count = db.session.query(Summary).count()
    amount = db.session.query(func.sum(Summary.amount)).scalar() or 0
    return count, amount
