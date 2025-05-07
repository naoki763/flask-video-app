# app/service/auth_service.py

from flask_login import login_user

from app.crud.user import get_user_by_username


def authenticate_and_login(username: str, password: str) -> bool:
    user = get_user_by_username(username)
    if user and user.check_password(password):
        login_user(user)
        return True
    return False
