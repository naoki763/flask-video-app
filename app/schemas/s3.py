# app/schemas/thumbnail_result.py

from datetime import datetime

from pydantic import BaseModel


# generate_thumbnailの戻り値の型を定義
class ThumbnailResult(BaseModel):
    thumbnail_url: str
    created_at: datetime


# upload_s3_for_videoの戻り値の型を定義
class UploadS3ForVideoResult(BaseModel):
    user_id: int
    title: str
    url: str
    thumbnail_url: str
    created_at: datetime
