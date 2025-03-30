from flask import current_app
from sqlalchemy import text
from app.extensions import db
from app.models import Summary

def handle_form_errors(form):
    for field in form._fields.values():
        for error in field.errors:
            current_app.logger.warning(
                f'⚠️ [FormValidation] {field.label.text}：{error}'
            )

def database_reset():
    try:
        db.session.query(Summary).delete()
        db.session.commit()
        db.session.execute(text('ALTER TABLE summaries AUTO_INCREMENT = 1;'))
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        current_app.logger.exception('❌ database_reset 失敗')
        return False
