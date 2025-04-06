from flask import Blueprint, render_template

license_bp = Blueprint('license', __name__)

@license_bp.route('/license')
def license():
    return render_template('license.html')
