from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField
from wtforms.validators import DataRequired, Regexp
from wtforms_alchemy import ModelForm

from app.models import Summary


class SummaryForm(FlaskForm, ModelForm):
    class Meta:
        model = Summary
        exclude = ['user_cognito_id', 'created_at', 'updated_at']

    tel = StringField('電話', validators=[
        Regexp(r'^\d*$', message='数字ではない文字が入力されました')
    ], render_kw={
        'pattern': r'^\d*$',
        'title': 'ハイフンなしの数字'
    })

class DeleteForm(FlaskForm):
    id = HiddenField('ID', validators=[DataRequired()])

class CSRFForm(FlaskForm):
    pass
