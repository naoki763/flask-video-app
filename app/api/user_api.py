from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.auth.decorators import roles_required
from app.crud.user import (
    create_user,
    delete_user_by_id,
    get_user_by_id,
    read_users,
    update_user_by_id,
)
from app.schemas.user import RegisterForm, UserUpdate
from app.service.user_service import create_userform_check


user_bp = Blueprint("user", __name__, url_prefix="/user")


# これでにユーザー管理画面に入れるぜ
@user_bp.route("/management", methods=["GET", "POST"])
@roles_required("Owner")  # 管理者権限が必要なルートを保護
def user_management() -> str:
    form = RegisterForm()
    if request.method == "POST":
        if not form.validate_on_submit():
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{field}:{error}", "danger")
            return redirect(url_for("user.user_management"))

        user = create_userform_check(form)
        if user is None:
            return redirect(url_for("user.user_management"))

        create_user(user)
        return redirect(url_for("user.user_management"))
    # ユーザー一覧を取得
    users = read_users()
    return render_template("user_management.html", users=users, form=form)


# 🔹 新規登録ページを表示（GET）
@user_bp.route("/register", methods=["GET"])
def new_register_form():
    form = RegisterForm()
    return render_template("new_register.html", form=form)


# 🔹 新規登録処理（POST）
@user_bp.route("/register", methods=["POST"])
def new_register_post():
    form = RegisterForm()

    if not form.validate_on_submit():
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}:{error}", "danger")
        return redirect(url_for("user.new_register_form"))

    user = create_userform_check(form)
    if user is None:
        return redirect(url_for("user.new_register_form"))

    create_user(user)
    return redirect(url_for("auth.login_form"))


# ユーザ情報更新
@user_bp.route("/user_management/<int:user_id>/update", methods=["GET", "POST"])
def update_user(user_id):
    if request.method == "GET":
        user = get_user_by_id(user_id)
        return render_template("edit_user.html", user=user)

    # POSTメソッドの処理
    user_form = UserUpdate(
        username=request.form.get("username", "").strip(),
        email=request.form.get("email", "").strip(),
        password=request.form.get("password", ""),
        role=request.form.get("role", "user").strip(),
    )
    updated_user = update_user_by_id(user_form, user_id)
    if updated_user is None:
        flash("ユーザー情報の更新に失敗しました", "danger")
        return redirect(url_for("user.user_management"))
    # 更新成功時の処理
    flash(f"{updated_user.username}様のユーザー情報を更新しました", "success")
    return redirect(url_for("user.user_management"))


@user_bp.route("/user_management/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = delete_user_by_id(user_id)
    if user is None:
        flash("ユーザーの削除に失敗しました", "danger")
        return redirect(url_for("user.user_management"))
    flash("ユーザーを削除しました", "success")
    return redirect(url_for("user.user_management"))
