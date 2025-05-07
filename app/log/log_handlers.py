import logging
import sys

import watchtower

from app.utils.timezone import convert_jst


def log_handler(app):
    logger = logging.getLogger()  # ルートロガー
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s]: %(message)s")
    formatter.converter = convert_jst

    # 標準出力
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # CloudWatch Logs
    cw_handler = watchtower.CloudWatchLogHandler(
        boto3_client=app.config["CLOUDWATCH_CLIENT"],
        log_group_name=app.config["LOG_GROUP"],
        log_stream_name=app.config["LOG_STREAM"],
        create_log_group=True,
        create_log_stream=True,
    )
    cw_handler.setFormatter(formatter)
    logger.addHandler(cw_handler)

    # Flaskのロガーにルートロガーの設定を引き継ぎ
    app.logger.handlers = logger.handlers
    app.logger.setLevel(logger.level)

    logger.info("CloudWatch Logsのハンドラが設定されました。")
