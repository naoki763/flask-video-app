# app/error_handlers.py
import logging

from flask import render_template, request


logger = logging.getLogger(__name__)


def error_404_handlers(app):
    @app.errorhandler(404)
    def page_not_found(e):
        logger.warning(f"404 Not Found: {request.path} にアクセスされました。 - {e}")
        return render_template("404.html"), 404

    # 他のエラーハンドラもここに追加可


def error_500_handlers(app):
    @app.errorhandler(500)
    def internal_server_error(e):
        logger.error(f"500 Internal Server Error:{e}")
        return render_template("500.html"), 500
