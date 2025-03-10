from wtforms import HiddenField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

class DeleteForm(FlaskForm):
    id = HiddenField("ID", validators=[DataRequired()])
