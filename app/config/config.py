from app.service.cloudwatch import (
    create_cloudwatch_client,
    create_localstack_cloudwatch_client,
)
from app.service.s3 import create_localstack_s3client, create_s3client
from app.utils.env import get_env_variable


# 環境変数を取得しflaskアプリに設定するためのクラス


class BaseConfig:
    # DB設定
    db_user = get_env_variable(key="DB_USER", default="video_user")
    db_pass = get_env_variable(key="DB_PASS", default="video_pass")
    db_host = get_env_variable(key="DB_HOST", default="host.docker.internal")
    db_port = get_env_variable(key="DB_PORT", default="5432")
    db_name = get_env_variable(key="DB_NAME", default="video_manager_db")
    secret_key = get_env_variable(key="DB_SECRET_KEY", default="dev")

    # DB初期値ユーザ
    adminuser = get_env_variable(key="ADMIN_USER", default="admin")
    adminpass = get_env_variable(key="ADMIN_PASS", default="admin1234")

    # s3設定
    bucket_name = get_env_variable(key="S3_BUCKET_NAME", default="my-video-bucket")
    region = get_env_variable(key="AWS_REGION", default="us-east-1")

    # CloudWatch設定
    log_group = get_env_variable(key="LOG_GROUP", default="video-log-group")
    log_stream = get_env_variable(key="LOG_STREAM", default="video-log-stream")

    # 環境変数の設定
    SECRET_KEY = secret_key
    ADMINUSER = adminuser
    ADMINPASS = adminpass
    S3_BUCKET_NAME = bucket_name
    LOG_GROUP = log_group
    LOG_STREAM = log_stream
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    )


# 開発用の環境変数設定
class DevelopmentConfig(BaseConfig):
    aws_access_key = get_env_variable(key="AWS_ACCESS_KEY_ID", default="test")
    aws_secret_access_key = get_env_variable(
        key="AWS_SECRET_ACCESS_KEY", default="test"
    )
    endpoint_url = get_env_variable(
        key="S3_ENDPOINT", default="http://host.docker.internal:4566"
    )
    public_host = get_env_variable(
        key="PUBLIC_ENDPOINT", default="http://localhost:4566"
    )
    url_host = f"{public_host}/{BaseConfig.bucket_name}"
    # create s3_client for localstack
    # 開発用のS3クライアント
    s3_client = create_localstack_s3client(
        BaseConfig.region, endpoint_url, aws_access_key, aws_secret_access_key
    )
    # 開発用のCloudWatchクライアント
    cloudwatch_client = create_localstack_cloudwatch_client(
        BaseConfig.region, endpoint_url, aws_access_key, aws_secret_access_key
    )

    # 環境変数の設定
    S3_HOST = url_host
    S3_CLIENT = s3_client
    CLOUDWATCH_CLIENT = cloudwatch_client


# 本番用の環境変数設定
class ProductionConfig(BaseConfig):
    # 本番用のS3クライアント
    s3_client = create_s3client(BaseConfig.region)
    # 本番用のCloudWatchクライアント
    cloudwatch_client = create_cloudwatch_client(BaseConfig.region)
    url_host = f"https://{BaseConfig.bucket_name}.s3.{BaseConfig.region}.amazonaws.com"

    # 環境変数の設定
    S3_HOST = url_host
    S3_CLIENT = s3_client
    CLOUDWATCH_CLIENT = cloudwatch_client
