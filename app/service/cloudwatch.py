import boto3


def create_localstack_cloudwatch_client(region, endpoint_url, access_key, secret_key):
    return boto3.client(
        "logs",
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
    )


def create_cloudwatch_client(region):
    return boto3.client(
        "logs",
        region_name=region,
    )
