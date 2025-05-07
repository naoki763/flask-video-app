from functools import wraps

from flask import abort
from flask_login import current_user, login_required


# def roles_required(f):
#     """管理者権限が必要なルートを保護するデコレータ"""

#     @wraps(f)
#     @login_required
#     def decorated_function(*args, **kwargs):
#         print(current_user.role)
#         if current_user.role != "Owner":
#             abort(403)
#         return f(*args, **kwargs)

#     return decorated_function


def roles_required(*roles):
    """指定したロールが必要なルートを保護するデコレータ"""

    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            print(f"現在のユーザー権限: {current_user.role}")
            if current_user.role not in roles:
                abort(404)
            return f(*args, **kwargs)

        return decorated_function

    return decorator
