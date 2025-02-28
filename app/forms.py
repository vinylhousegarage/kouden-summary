from app.models import Summary
from app.extensions import db
from wtforms_alchemy import ModelForm

class SummaryForm(ModelForm):
    class Meta:
        model = Summary
        sqlalchemy_session = db.session
