from app.extensions import db
from app.models import Summary

def database_reset():
    try:
        db.session.query(Summary).delete()
        db.session.commit()

        db.session.execute('ALTER TABLE summary AUTO_INCREMENT = 1;')
        db.session.commit()

        return True

    except Exception as e:
        db.session.rollback()
        print(f'Error in database_reset: {e}')
        return False
