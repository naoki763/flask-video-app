import boto3


# 定数（設定に応じて調整）
LOCALSTACK_ENDPOINT = "http://host.docker.internal:4566"
S3_BUCKET_NAME = "my-video-bucket"
AWS_REGION = "us-east-1"
AWS_ACCESS_KEY_ID = "test"
AWS_SECRET_ACCESS_KEY = "test"

# S3クライアント作成（LocalStack向け）
s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
    endpoint_url=LOCALSTACK_ENDPOINT,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


# バケット作成
try:
    s3_client.create_bucket(Bucket=S3_BUCKET_NAME)
    print("success create s3 bucket")
except s3_client.exceptions.ClientError as e:
    print(f"Bucket already exists or error: {e}")
