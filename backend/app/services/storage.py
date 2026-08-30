"""S3-compatible object storage client for Cloudflare R2."""

import boto3

from app.core.config import settings

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = boto3.client(
            "s3",
            endpoint_url=(f"https://{settings.R2_ACCOUNT_ID}.r2.cloudflarestorage.com"),
            aws_access_key_id=settings.R2_ACCESS_KEY_ID,
            aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
            region_name="auto",
        )
    return _client


def upload_object(key: str, data: bytes) -> None:
    _get_client().put_object(Bucket=settings.R2_BUCKET_NAME, Key=key, Body=data)


def download_object(key: str) -> bytes:
    response = _get_client().get_object(Bucket=settings.R2_BUCKET_NAME, Key=key)
    return response["Body"].read()


def delete_object(key: str) -> None:
    _get_client().delete_object(Bucket=settings.R2_BUCKET_NAME, Key=key)
