import sys
from sqlalchemy import text
from app.extensions import db
from app.models import Summary

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
