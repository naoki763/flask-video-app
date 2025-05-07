# app/forms/video_form.py
from flask import flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField
from wtforms.validators import Length

from app.schemas.validators import file_not_empty


# ブラウザからのリクエストを検証するためのフォーム
class VideoUploadForm(FlaskForm):
    title = StringField("タイトル", validators=[Length(max=100)])
    file = FileField(
        "動画ファイル",
        validators=[
            FileRequired(message="動画ファイルは必須です。"),
            file_not_empty(),
            # FileAllowed(
            #     ["mp4", "mov", "avi", "mts", "m2ts"],
            #     "動画ファイルのみ許可されています。",
            # ),
        ],
    )

    def validate(self, extra_validators=None):
        is_valid = super().validate(extra_validators)
        if not is_valid:
            for field_name, errors in self.errors.items():
                label = getattr(self, field_name).label.text
                for error in errors:
                    flash(f"{label}: {error}", "danger")
        return is_valid
