import logging

import ffmpeg

from app.schemas.s3 import ThumbnailResult
from app.service.s3 import upload_s3
from app.service.video_utils import delete_temp_file, generate_s3_url, get_creation_time


logger = logging.getLogger(__name__)


def generate_thumbnail(tmp_path, unique_filename, time_seconds=1):
    thumbnail_filename = unique_filename.rsplit(".", 1)[0] + ".jpg"
    thumbnail_path = f"/tmp/{thumbnail_filename}"
    try:
        (
            ffmpeg.input(tmp_path, ss=time_seconds)  # 指定秒から
            .output(thumbnail_path, vframes=1)  # 1フレームだけ出力
            .run()
        )
        print(f"✅ サムネイル生成完了: {thumbnail_path}")

        with open(thumbnail_path, "rb") as thumb_file:
            upload_s3(thumb_file, f"thumbnails/{thumbnail_filename}")

        # DBに保存するためのURLと投稿日時(メタデータ取得)を生成
        thumbnail_url = generate_s3_url(f"thumbnails/{thumbnail_filename}")
        creation_time = get_creation_time(tmp_path)
        return ThumbnailResult(
            thumbnail_url=thumbnail_url,
            created_at=creation_time,
        )

    except ffmpeg.Error as ffe:
        logger.error(f"ffmpegエラー: {ffe}")

    except Exception as e:
        logger.error(f"予期しないエラー: {e}")

    finally:
        # 🔥 一時ファイルのクリーンアップ
        delete_temp_file(thumbnail_path)
