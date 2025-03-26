import sys
from flask import flash, current_app
from sqlalchemy import text
from app.extensions import db
from app.models import Summary

def handle_form_errors(form):
    for field in form._fields.values():
        for error in field.errors:
            message = f"{field.label.text}：{error}"
            flash(message)
            current_app.logger.warning(message)

def database_reset():
    try:
        db.session.query(Summary).delete()
        db.session.commit()

        db.session.execute(text('ALTER TABLE summaries AUTO_INCREMENT = 1;'))
        db.session.commit()

        return True

    except Exception as e:
        db.session.rollback()
        print(f'Error in database_reset: {e}', file=sys.stderr, flush=True)
        return False
