import logging

from flask import abort
from flask_login import current_user

from app.schemas.s3 import UploadS3ForVideoResult
from app.service.s3 import delete_s3, upload_s3
from app.service.thumbnail_generator import generate_thumbnail
from app.service.video_utils import (
    delete_temp_file,
    extract_key_from_url,
    generate_s3_url,
    generate_unique_filename,
    save_temp_video,
)


logger = logging.getLogger(__name__)


def upload_s3_for_video(file, title):
    filename = generate_unique_filename(file.filename)
    file_url = generate_s3_url(filename)
    tmp_path = None

    try:
        # 動画ファイルを一時的に保存
        # 以後は一時保存先のパスを使って処理
        tmp_path = save_temp_video(file, filename)
        with open(tmp_path, "rb") as f:
            upload_s3(f, filename)

        # ---サムネイル生成---
        thumbnail_result = generate_thumbnail(tmp_path, filename)

        return UploadS3ForVideoResult(
            user_id=current_user.id,
            title=title,
            url=file_url,
            thumbnail_url=thumbnail_result.thumbnail_url,
            created_at=thumbnail_result.created_at,
        )
    except Exception as e:
        logger.error(f"予期しないエラー: {e}")
        abort(500)
    finally:
        if tmp_path:
            # 🔥 一時ファイルのクリーンアップ
            delete_temp_file(tmp_path)


def delete_s3_for_video(video_url, thumbnail_url):
    video_key = extract_key_from_url(video_url)
    thumbnail_key = extract_key_from_url(thumbnail_url)

    delete_s3(video_key)
    delete_s3(thumbnail_key)
