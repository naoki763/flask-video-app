import logging

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from flask import current_app


logger = logging.getLogger(__name__)


# 開発環境用s3クライアント
def create_localstack_s3client(region, endpoint_url, access_key, secret_key):
    return boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
    )


# 本番環境用s3クライアント
def create_s3client(region):
    return boto3.client(
        "s3",
        region_name=region,
    )


def upload_s3(file, filename):
    try:
        s3 = current_app.config["S3_CLIENT"]
        bucket_name = current_app.config["S3_BUCKET_NAME"]
        file.seek(0)  # 🔥 これが命綱
        s3.upload_fileobj(file, bucket_name, filename)
    except (BotoCoreError, ClientError) as be:
        logger.error(f"S3アップロード失敗: {filename} - {be}")
    except Exception as e:
        logger.error(f"予期しないエラー: {e}")


def delete_s3(key):
    try:
        s3 = current_app.config["S3_CLIENT"]
        bucket_name = current_app.config["S3_BUCKET_NAME"]
        s3.delete_object(Bucket=bucket_name, Key=key)
    except (BotoCoreError, ClientError) as be:
        logger.error(f"S3デリート失敗: {key} - {be}")
    except Exception as e:
        logger.error(f"予期しないエラー: {e}")
