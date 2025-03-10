from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, Regexp
from wtforms_alchemy import ModelForm
from app.models import Summary

class CreateForm(ModelForm):
    class Meta:
        model = Summary
        exclude = ["user_cognito_id", "created_at"]

    giver_name = StringField("名前", validators=[DataRequired(), Length(max=100)])
    amount = IntegerField("金額", validators=[DataRequired(), NumberRange(min=1)])
    address = StringField("住所", validators=[Length(max=250)])
    tel = StringField("電話", validators=[
        Length(max=20),
        Regexp(r"^\+?\d{1,15}$", message="電話番号は数値のみ（+含む）で入力してください")
    ])
    note = StringField("備考", validators=[Length(max=250)])
