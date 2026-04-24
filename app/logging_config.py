import logging


def get_log_level(app):
    level_str = app.config.get("LOG_LEVEL", "INFO").upper()
    return getattr(logging, level_str, logging.INFO)

def setup_logging(app):
    log_level = get_log_level(app)

    app.logger.setLevel(log_level)

    if app.logger.hasHandlers():
        for handler in app.logger.handlers:
            handler.setLevel(log_level)
        app.logger.info(f'✅ 既存の `handler` を使用 (level={log_level})')
    else:
        handler = logging.StreamHandler()
        handler.setLevel(log_level)

        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s')
        handler.setFormatter(formatter)

        app.logger.addHandler(handler)
        app.logger.info(f'✅ `handler` を新規作成 (level={log_level})')

    app.logger.info('✅ logging 設定完了')
