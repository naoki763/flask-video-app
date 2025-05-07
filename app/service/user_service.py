from flask import flash
from werkzeug.security import generate_password_hash

from app.crud.user import get_user_by_email
from app.schemas.user import UserCreate


def create_userform_check(form):
    try:
        # フォームバリデーション後の追加検証
        if not all([form.username.data, form.email.data, form.password.data]):
            flash("全ての項目を入力してください", "error")
            return None

        if get_user_by_email(form.email.data):
            flash("このメールアドレスは既に登録されています", "error")
            return None

        hashed_pw = generate_password_hash(form.password.data)
        user = UserCreate(
            username=form.username.data, email=form.email.data, password=hashed_pw
        )
        if user:
            flash("新規登録が完了しました！", "success")
        return user

    except Exception:
        flash("登録中にエラーが発生しました", "error")
        return None
