import pymysql

from flask import current_app

from app.config import Config


_mediumblob_checked = False

def ensure_mediumblob():
    global _mediumblob_checked
    if _mediumblob_checked:
        return

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
            current_app.logger.info('✅ `sessions` テーブルが存在するので ALTER TABLE 実行')

            cursor.execute("SHOW COLUMNS FROM sessions LIKE 'data'")
            column_info = cursor.fetchone()
            if column_info and 'mediumblob' not in column_info[1].lower():
                current_app.logger.info('✅ `data` カラムを `MEDIUMBLOB` に変更')

                cursor.execute('ALTER TABLE sessions MODIFY data MEDIUMBLOB')
                conn.commit()
            else:
                current_app.logger.info('✅ `data` カラムはすでに `MEDIUMBLOB`')
        else:
            current_app.logger.warning('⚠️ `sessions` テーブルがまだ作成されていません')
        _mediumblob_checked = True
    except Exception:
        current_app.logger.exception('❌ ALTER TABLE 実行中にエラー発生')
    finally:
        conn.close()
