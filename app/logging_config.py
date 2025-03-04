import logging
import sys

def check_existing_handlers(app):
    print(f"📌 app.logger の現在の `handlers`:\n{app.logger.handlers}", file=sys.stderr, flush=True)

    for handler in app.logger.handlers:
        print(f"🔹 ハンドラーのタイプ: {type(handler)}", file=sys.stderr, flush=True)
        print(f"🔹 ログレベル: {handler.level}", file=sys.stderr, flush=True)

def setup_logging(app):
    app.logger.setLevel(logging.DEBUG)

    if app.logger.hasHandlers():
        for handler in app.logger.handlers:
            handler.setLevel(logging.DEBUG)
        app.logger.debug("🔹 既存の `handler` を使用しました。")
    else:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] - %(message)s")
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)
        app.logger.debug("🆕 `handler` を新しく追加しました。")

    app.logger.info("✅ Flask アプリのロギングが設定されました。")
