from wtforms import StringField, HiddenField
from wtforms.validators import Regexp, DataRequired
from flask_wtf import FlaskForm
from wtforms_alchemy import ModelForm
from app.models import Summary

class SummaryForm(FlaskForm, ModelForm):
    class Meta:
        model = Summary
        exclude = ['user_cognito_id', 'created_at', 'updated_at']

    tel = StringField('電話', validators=[
        Regexp(r'^\d*$', message='数字のみで入力してください')
    ])

class DeleteForm(FlaskForm):
    id = HiddenField('ID', validators=[DataRequired()])

class CSRFForm(FlaskForm):
    pass
