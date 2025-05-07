from collections import defaultdict
import logging

from flask import abort
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from app.models.models import Comment, Video, db


logger = logging.getLogger(__name__)


# 動画をすべて取得
def get_all_videos():
    try:
        videos = Video.query.order_by(Video.created_at.desc()).all()
        return videos
    except SQLAlchemyError as se:
        logger.error(f"SQLAlchemy error reading all videos: {se}")
        abort(500)
    except Exception as e:
        logger.error(f"予期しないエラー: {e}")
        abort(500)


# 動画をIDで取得する関数
def get_video_by_id(video_id):
    try:
        video = Video.query.filter_by(id=video_id).first()
        if video is None:
            logger.warning(f"Video with ID {video_id} not found.")
        return video
    except SQLAlchemyError as se:
        logger.error(f"SQLAlchemy error reading video with ID {video_id}: {se}")
        abort(500)
    except Exception as e:
        logger.error(f"予期しないエラー: {e}")
        abort(500)


# 動画とコメントを取得する関数
def get_video_with_comments(video_id):
    try:
        video = (
            Video.query.options(joinedload(Video.comments).joinedload(Comment.user))
            .filter_by(id=video_id)
            .first()
        )
        if video is None:
            logger.warnninng(f"Video with ID {video_id} not found.")
        return video
    except SQLAlchemyError as se:
        logger.error(f"SQLAlchemy error reading video with ID {video_id}: {se}")
        abort(500)
    except Exception as e:
        logger.error(f"予期しないエラー: {e}")
        abort(500)


# 動画をyear毎に取得する関数
def get_videos_by_year(year) -> list:
    try:
        videos = (
            Video.query.filter(Video.created_at != None)
            .filter(db.extract("year", Video.created_at) == year)
            .order_by(Video.created_at.desc())
            .all()
        )
        return videos
    except SQLAlchemyError as se:
        logger.error(f"SQLAlchemy error reading videos for year {year}: {se}")
        abort(500)
    except Exception as e:
        logger.error(f"予期しないエラー: {e}")
        abort(500)


# 動画を月毎の辞書型に変更する関数
def group_videos_by_month(videos: list) -> dict:
    videos_by_month = defaultdict(list)
    for video in videos:
        month = video.created_at.month
        videos_by_month[month].append(video)
    return videos_by_month


# 動画の撮影日毎に「年」を取得する関数
def get_years_available() -> list:
    years = {
        video.created_at.year for video in Video.query.filter(Video.created_at != None)
    }
    return sorted(years, reverse=True)


# 動画データをDBに保存する関数
def create_video(video_data):
    try:
        video = Video(**video_data.dict())
        db.session.add(video)
        db.session.commit()
    except SQLAlchemyError as se:
        logger.error(f"SQLAlchemy error creating video: {se}")
        db.session.rollback()
        abort(500)
    except Exception as e:
        logger.error(f"予期しないエラー: {e}")
        db.session.rollback()
        abort(500)


# 動画データをDBから削除する関数
def delete_video_by_id(video_id):
    try:
        video = get_video_by_id(video_id)
        db.session.delete(video)
        db.session.commit()
    except SQLAlchemyError as se:
        logger.error(f"SQLAlchemy error deleting video with ID {video_id}: {se}")
        db.session.rollback()
        abort(500)
    except Exception as e:
        logger.error(f"予期しないエラー: {e}")
        db.session.rollback()
        abort(500)
