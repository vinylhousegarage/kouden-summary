import logging

def check_existing_handlers(app):
    app.logger.info(f'✅ app.logger の現在の `handlers`:\n{app.logger.handlers}')

    for handler in app.logger.handlers:
        app.logger.info(f'✅ ハンドラーのタイプ: {type(handler)}')
        app.logger.info(f'✅ ログレベル: {handler.level}')

def setup_logging(app):
    app.logger.setLevel(logging.INFO)

    if app.logger.hasHandlers():
        for handler in app.logger.handlers:
            handler.setLevel(logging.INFO)
        app.logger.info('✅ 既存の `handler` を使用')
    else:
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s')
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)
        app.logger.info('✅ `handler` を新規作成')

    app.logger.info('✅ logging 設定完了')
