from flask import Blueprint, render_template, session

from app.forms import CSRFForm
from app.utils.auth_helpers import redirect_to_cognito_login

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def main():
    if 'access_token' not in session:
        return redirect_to_cognito_login()

    form = CSRFForm()
    return render_template('dashboard.html', form=form)
