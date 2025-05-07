from os import error

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user
from flask_migrate import Migrate

from app.config.config import DevelopmentConfig, ProductionConfig
from app.error.error_handlers import error_404_handlers, error_500_handlers
from app.extensions import migrate
from app.log.log_handlers import log_handler
from app.models.models import User, db
from app.utils.env import get_env_variable


def create_app():
    try:
        app = Flask(__name__)  # ここでアプリが作成される

        # 環境切り替え用にENVを取得
        env = get_env_variable(key="ENV", default="local")

        # 開発環境と本番環境の切り替え
        if env == "local":
            print("開発用")
            # 環境毎に異なる.envファイルを読み込む
            env_file = f".env.{env}"
            load_dotenv(env_file)

            app.config.from_object(DevelopmentConfig)

        else:
            print("本番用")
            app.config.from_object(ProductionConfig)

        # Initialize the database
        db.init_app(app)
        # Initialize the table
        with app.app_context():
            from app.models import models

            db.create_all()  # ここでテーブルを作成

        migrate.init_app(app, db)

        # ********************************
        # DB初期値設定
        with app.app_context():
            from werkzeug.security import generate_password_hash

            existing_user = models.User.query.filter_by(username="admin").first()
            if not existing_user:
                admin = models.User(
                    username=app.config["ADMINUSER"],
                    password=generate_password_hash(app.config["ADMINPASS"]),
                    email="admin@example.com",
                    role="Owner",
                )
                db.session.add(admin)
                db.session.commit()
                print("Adminユーザーを初期作成しました")
            else:
                print("Adminユーザーはすでに存在します")
        # ********************************

        # 各種ハンドラー設定
        # エラーハンドラ
        error_404_handlers(app)  # 404エラーハンドラを登録
        error_500_handlers(app)  # 500エラーハンドラを登録

        # ログハンドラ()
        log_handler(app)

        # Flask-Login のセットアップ
        login_manager = LoginManager()
        login_manager.init_app(app)
        login_manager.login_view = (
            "login.login_form"  # ログインページのエンドポイントを指定
        )

        @login_manager.user_loader  # コールバック関数で
        def load_user(user_id):
            return User.query.get(
                int(user_id)
            )  # ユーザー情報をDBから取得　この関数は 「ログイン状態のユーザーを取得する」 必要があるときに、Flask-Login が自動的に呼び出す

        # app.api.routes` のように `app.api` を経由しないで、直接モジュールを指定、/app/api__init__.pyで管理すると３つ書かなくてもよくなる
        from app.api.comment_api import comment_bp
        from app.api.login_api import login_bp
        from app.api.routes import home_bp
        from app.api.user_api import user_bp
        from app.api.video_api import video_bp

        # Blueprintの登録
        app.register_blueprint(login_bp, url_prefix="/auth")  # /loginに関するBP
        app.register_blueprint(home_bp, url_prefix="")  # / URLに入った時の最初のページ
        app.register_blueprint(user_bp, url_prefix="/user")
        app.register_blueprint(video_bp, url_prefix="/video")
        app.register_blueprint(comment_bp, url_prefix="/comment")

        # 未ログインユーザを強制的にログインページにリダイレクト
        @app.before_request
        def require_login():
            allowed_routes = [
                "auth.login",
                "auth.login_form",
                "user.new_register_form",
                "user.new_register_post",
                "home.health_check",
            ]
            if (
                not current_user.is_authenticated
                and request.endpoint not in allowed_routes
            ):
                return redirect(url_for("auth.login_form"))

        app.logger.info("アプリケーションが起動しました")
        return app
    except Exception as e:
        app.logger.error(f"Error: {e}")
        print(f"Error: {e}")
        print("*******")
        raise e
