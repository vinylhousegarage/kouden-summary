import pymysql
import logging
from flask import session, current_app
from app.config import Config

def ensure_mediumblob():
    with current_app.app_context():
        session['init'] = 'dummy'

        try:
            conn = pymysql.connect(
                host=Config.DB_HOST,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME
            )
            cursor = conn.cursor()

            cursor.execute("SHOW TABLES LIKE 'sessions'")
            if cursor.fetchone():
                print('✅ sessions テーブルが存在するので ALTER TABLE 実行')
                cursor.execute('ALTER TABLE sessions MODIFY data MEDIUMBLOB')
                conn.commit()
            else:
                print('⚠️ sessions テーブルが作成されませんでした')

        except Exception as e:
            logging.error(f'❌ ensure_mediumblob() 実行中にエラー発生: {e}')
        finally:
            conn.close()
