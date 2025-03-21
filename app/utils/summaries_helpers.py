from app.extensions import db
from app.models import Summary

def database_reset():
    try:
        db.session.query(Summary).delete()
        db.session.commit()

        db.session.execute('ALTER SEQUENCE summary_id_seq RESTART WITH 1;')
        db.session.commit()

        return True

    except Exception as e:
        db.session.rollback()
        print(f'Error: {e}')
        return False
