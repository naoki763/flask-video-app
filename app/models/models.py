from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash


db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="Member")

    videos: Mapped[list["Video"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(
            self.password, password
        )  # パスワードチェックの実装を後で修正することを推奨


class Video(db.Model):
    __tablename__ = "video"

    id: Mapped[int] = mapped_column(primary_key=True)
    # uuid: Mapped[UUID] = mapped_column(
    #     PG_UUID(as_uuid=True), unique=True, nullable=False, default=uuid4
    # )
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    thumbnail_url: Mapped[str] = mapped_column(String(255), nullable=True)
    posted_at: Mapped[datetime] = mapped_column(nullable=False, default=func.now())
    # 動画のメタデータ保存用のカラムを追加
    created_at: Mapped[datetime] = mapped_column(nullable=True)

    user: Mapped["User"] = relationship(back_populates="videos")
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="video", cascade="all, delete-orphan"
    )


class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    video_id: Mapped[int] = mapped_column(ForeignKey("video.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    content: Mapped[str] = mapped_column(String(255), nullable=False)
    posted_at: Mapped[datetime] = mapped_column(nullable=False, default=func.now())

    video: Mapped["Video"] = relationship(back_populates="comments")
    user: Mapped["User"] = relationship(back_populates="comments", lazy="joined")
