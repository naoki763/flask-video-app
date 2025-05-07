from datetime import datetime, timedelta, timezone
import time


# 日本のタイムゾーンを定義
JST = timezone(timedelta(hours=+9), name="Asia/Tokyo")


def now_jst():
    # datetimeオブジェクトでJSTの現在時刻を返す
    return datetime.now(JST)


def convert_jst(timestamp):
    # formatter用JSTコンバーター
    return time.localtime(timestamp + 9 * 3600)
