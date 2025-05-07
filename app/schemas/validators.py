from wtforms.validators import ValidationError


# ファイルサイズが0バイトのバリデーション
def file_not_empty():
    def _file_not_empty(form, field):
        file = field.data
        if file and hasattr(file, "stream"):
            file.stream.seek(0, 2)  # ファイルの末尾に移動
            size = file.stream.tell()
            file.stream.seek(0)  # 元に戻す
            if size == 0:
                raise ValidationError("ファイルサイズが0バイトです。")

    return _file_not_empty


# フォーム内の空白のバリデーション
def no_space(form, field):
    if " " in field.data:
        raise ValidationError("スペースは使えません。")
