from flask import Blueprint, render_template

license_bp = Blueprint('license', __name__)

@license_bp.route('/license')
def license_page():
    return render_template('license.html')
