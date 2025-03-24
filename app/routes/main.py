from flask import Blueprint, session, render_template
from app.utils.auth_helpers import redirect_to_cognito_login
from app.models import Summary
from app.forms import CSRFForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def main():
    if 'access_token' not in session:
        return redirect_to_cognito_login()

    summaries = Summary.query.all()
    form = CSRFForm()

    return render_template('dashboard.html', summaries=summaries, form=form)
