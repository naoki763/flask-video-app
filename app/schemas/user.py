# 修正後（Ruff推奨スタイル）
from flask_wtf import FlaskForm
from pydantic import BaseModel
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, Length

from app.schemas.validators import no_space


class RegisterForm(FlaskForm):
    username = StringField(
        "ユーザー名",
        validators=[
            DataRequired(),
            Length(min=3, max=50),
            no_space,
        ],
    )
    email = StringField(
        "メールアドレス", validators=[DataRequired(), Email(), no_space]
    )
    password = PasswordField(
        "パスワード",
        validators=[
            DataRequired(),
            Length(min=8, message="パスワードは8文字以上！"),
            no_space,
        ],
    )
    # role = SelectField("権限", choices=[("Owner", "Owner"), ("Member", "Member")])


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str | None = None

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    role: str | None = None

    class Config:
        from_attributes = True
