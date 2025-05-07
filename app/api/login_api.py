from flask import Blueprint, flash, redirect, render_template, session, url_for
from flask_login import login_required, logout_user

from app.auth.auth_service import authenticate_and_login
from app.schemas.auth import LoginForm


login_bp = Blueprint("auth", __name__, url_prefix="/auth")


# 画面の表示
@login_bp.route("/login", methods=["GET"])
def login_form():
    form = LoginForm()
    return render_template("login.html", form=form)


# ログイン時のIDとpassの受け取り
@login_bp.route("/login", methods=["POST"])
def login():
    form = LoginForm()

    # username = request.form["username"]  # name="userid"の値がここに入る
    # password = request.form["password"]  # name="userid"の値がここに入る

    # user = User.query.filter_by(
    #     username=username
    # ).first()  # データベースからユーザー取得

    if form.validate_on_submit():
        if authenticate_and_login(form.username.data, form.password.data):
            return redirect(url_for("home.home"))
        flash("ログイン失敗。お前はログインのセンスがねぇーぜ！", "danger")
    else:
        flash("入力内容にエラーがあります。", "warning")

    return redirect(url_for("auth.login_form"))


# ✅ ログアウトAPI
@login_bp.route("/logout")
@login_required  # ログインしている人だけがアクセスできるようにする
def logout():
    logout_user()  # Flask-Loginのログアウト関数
    session.clear()  # ✅ セッションの完全クリア
    flash("ログアウトしました。")
    return redirect(url_for("auth.login_form"))  # ログイン画面にリダイレクト
