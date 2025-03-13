from flask_wtf import FlaskForm
from wtforms import HiddenField
from wtforms.validators import DataRequired
from wtforms_alchemy import ModelForm
from app.models import Summary

class SummaryForm(ModelForm):
    class Meta:
        model = Summary
        exclude = ["user_cognito_id", "created_at"]

class DeleteForm(FlaskForm):
    id = HiddenField("ID", validators=[DataRequired()])
