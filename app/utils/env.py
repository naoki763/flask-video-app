import os


def get_env_variable(key: str, default=None):
    # 環境変数から値を取得あ
    value = os.getenv(key=key)

    if value is None:
        return default
    else:
        return value
