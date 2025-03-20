import pymysql
import sys
import logging
from app.config import Config

def ensure_mediumblob():
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
            print('✅ `sessions` テーブルが存在するので ALTER TABLE 実行')

            cursor.execute("SHOW COLUMNS FROM sessions LIKE 'data'")
            column_info = cursor.fetchone()

            if column_info and 'mediumblob' not in column_info[1].lower():
                print('✅ `data` カラムを `MEDIUMBLOB` に変更', file=sys.stderr, flush=True)
                cursor.execute('ALTER TABLE sessions MODIFY data MEDIUMBLOB')
                conn.commit()
            else:
                print('✅ `data` カラムはすでに `MEDIUMBLOB`', file=sys.stderr, flush=True)
        else:
            print('⚠️ `sessions` テーブルがまだ作成されていません', file=sys.stderr, flush=True)

    except Exception as e:
        logging.error(f'❌ ALTER TABLE 実行中にエラー発生: {e}')
    finally:
        conn.close()
