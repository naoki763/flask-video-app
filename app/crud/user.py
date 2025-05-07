import logging

from flask import flash
from sqlalchemy.exc import SQLAlchemyError

from app.models.models import User, db
from app.schemas.user import UserUpdate


logger = logging.getLogger(__name__)


# # これどこかで使ってる？
# def get_videos_sorted_by_date():
#     return (
#         Video.query.filter(Video.created_at != None)
#         .order_by(Video.created_at.desc())
#         .all()
#     )


# # これどこかで使ってる？
# def group_videos_by_year_month(videos):
#     videos_by_year_month = defaultdict(lambda: defaultdict(list))
#     for video in videos:
#         year = video.created_at.year
#         month = video.created_at.month
#         videos_by_year_month[year][month].append(video)
#     return videos_by_year_month


# ユーザ一覧を取得
def read_users():
    try:
        return User.query.all()
    except SQLAlchemyError as se:
        logger.error(f"ユーザ一覧取得中にでエラーが発生しました。: {se}")
    except Exception as e:
        logger.error(f"予期しないエラー: {e}")


# idでuser情報を取得
def get_user_by_id(user_id: int):
    try:
        user = User.query.filter_by(id=user_id).first()
        if user:
            return user
        else:
            return None
    except SQLAlchemyError as se:
        logger.error(f"idによるユーザ情報取得中にでエラーが発生しました。: {se}")
    except Exception as e:
        logger.error(f"予期しないエラー: {e}")


# usernameでuser情報を取得
def get_user_by_username(username: str):
    try:
        user = User.query.filter_by(username=username).first()
        if user:
            return user
        else:
            return None
    except SQLAlchemyError as se:
        logger.error(f"usernameによるユーザ情報取得中にでエラーが発生しました。: {se}")
    except Exception as e:
        logger.error(f"予期しないエラー: {e}")


# メールアドレスからユーザ情報を取得
def get_user_by_email(email: str):
    try:
        user = User.query.filter_by(email=email).first()
        if user:
            return user
        else:
            return None
    except SQLAlchemyError as se:
        logger.error(
            f"メールアドレスによるユーザ情報取得中にでエラーが発生しました。: {se}"
        )
    except Exception as e:
        logger.error(f"予期しないエラー: {e}")


def create_user(usercreate):
    try:
        new_user = User(**usercreate.dict())
        db.session.add(new_user)
        db.session.commit()
        flash("登録成功！おまえはセンスあるぜ！", "success")
        return new_user

    except SQLAlchemyError as se:
        db.session.rollback()
        logger.error(f"データベースエラーを起こすな、おらぁ: {se}")
    except Exception as e:
        logger.error(f"このエラーは予期してなかったんだ、、、: {e}")


def update_user_by_id(userform: UserUpdate, user_id: int):
    try:
        user = User.query.filter_by(id=user_id).first()
        if user:
            # ユーザー情報を更新
            user.username = userform.username
            user.email = userform.email
            if userform.password:
                user.set_password(userform.password)
            user.role = userform.role

            db.session.commit()
            return user
        else:
            logger.warning("存在しないユーザが更新されようとしました")
            flash("そのユーザーは存在しないよ。責任者呼んでくれ")
            return None
    except SQLAlchemyError as se:
        db.session.rollback()
        logger.error(f"ユーザ更新でデータベースエラーが発生したよ: {se}")
    except Exception as e:
        logger.error(f"ユーザ更新で予期しないエラーが発生したよ: {e}")


def delete_user_by_id(user_id: int):
    try:
        user = User.query.filter_by(id=user_id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return user
        else:
            flash("そのユーザーは存在しないよ", "error")
            logger.warning(f"存在しないユーザが削除されようとしました:{user.username}")
            return None
    except SQLAlchemyError as se:
        db.session.rollback()
        logger.error(f"ユーザ削除でデータベースエラーが発生したよ: {se}")
    except Exception as e:
        logger.error(f"ユーザ削除で予期しないエラーが発生したよ: {e}")
