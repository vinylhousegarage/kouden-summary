from app.models import User, Summary
from app.extensions import db
from wtforms_alchemy import ModelForm

class UserForm(ModelForm):
    class Meta:
        model = User
        sqlalchemy_session = db.session

class SummaryForm(ModelForm):
    class Meta:
        model = Summary
        sqlalchemy_session = db.session
