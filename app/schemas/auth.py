# app/forms/login_form.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField("ユーザー名", validators=[DataRequired(), Length(max=50)])
    password = PasswordField("パスワード", validators=[DataRequired()])
