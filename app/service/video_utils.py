from datetime import datetime
import json
import logging
import os
import subprocess
from urllib.parse import urlparse
import uuid  # UUIDでユニークなIDをつける

from flask import current_app
from werkzeug.utils import secure_filename


logger = logging.getLogger(__name__)


# 動画アップロード用の位置なファイル名を設定
def generate_unique_filename(filename):
    unique_filename = f"{uuid.uuid4()}_{secure_filename(filename)}"
    return unique_filename


# s3に保存する動画にアクセスするURLを取得する
def generate_s3_url(filename):
    url_host = current_app.config["S3_HOST"]
    url = f"{url_host}/{filename}"
    return url


# S3のURLからkeyを抽出する関数
def extract_key_from_url(url):
    bucket_name = current_app.config["S3_BUCKET_NAME"]
    parsed = urlparse(url)
    url_path = parsed.path.lstrip("/")  # URLのパス部分を取得
    print(url_path)

    # localstackの場合
    if url_path.startswith(f"{bucket_name}/"):
        print(url_path[len(bucket_name) + 1 :])
        return url_path[len(bucket_name) + 1 :]
    # 本番環境の場合
    print(url_path)
    return url_path


# 動画ファイルからメタデータを取得
def get_creation_time(file_path) -> datetime | None:
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "quiet",
                "-print_format",
                "json",
                "-show_entries",
                "format_tags=creation_time",
                file_path,
            ],
            capture_output=True,
            text=True,
        )

        data = json.loads(result.stdout)
        creation_time_str = data["format"]["tags"]["creation_time"]

        try:
            # ISO 8601 → datetime変換（ZはUTC指定なので置換）
            return datetime.fromisoformat(creation_time_str.replace("Z", "+00:00"))
        except Exception as e:
            logger.warning(f"⛔ created_at の変換に失敗: {e}")
            return None

    except Exception as e:
        logger.warning(f"creation_time 取得失敗: {e}")
        return None


# 動画ファイルを一時的に保存し、ファイルパスを返す
def save_temp_video(file, filename):
    try:
        # 一時的な動画ファイルのパスを生成
        temp_video_path = f"/tmp/{filename}"
        file.save(temp_video_path)  # 一時的に動画を保存
        logger.info("ファイル保存成功")
        return temp_video_path
    except Exception as e:
        logger.error(f"一時ファイル保存失敗: {filename} - {e}")


# 一時ファイルを安全に削除する
def delete_temp_file(path: str):
    try:
        if os.path.exists(path):
            os.remove(path)
            logger.info("一時ファイル削除成功")
        else:
            logger.warning(f"一時ファイルが存在しません: {path}")
    except Exception as e:
        logger.error(f"一時ファイル削除失敗: {path} - {e}")
