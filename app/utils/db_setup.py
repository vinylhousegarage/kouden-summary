import pymysql
from app.config import Config

def ensure_mediumblob(app):
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
            app.logger.info('✅ `sessions` テーブルが存在するので ALTER TABLE 実行')

            cursor.execute("SHOW COLUMNS FROM sessions LIKE 'data'")
            column_info = cursor.fetchone()
            if column_info and 'mediumblob' not in column_info[1].lower():
                app.logger.info('✅ `data` カラムを `MEDIUMBLOB` に変更')

                cursor.execute('ALTER TABLE sessions MODIFY data MEDIUMBLOB')
                conn.commit()
            else:
                app.logger.info('✅ `data` カラムはすでに `MEDIUMBLOB`')
        else:
            app.logger.warning('⚠️ `sessions` テーブルがまだ作成されていません')
    except Exception:
        app.logger.exception('❌ ALTER TABLE 実行中にエラー発生')
    finally:
        conn.close()
