from flask import Blueprint, jsonify, render_template

from app.models.models import Video


home_bp = Blueprint(
    "home", __name__
)  # url_prefix=""を追加してもいいか、特に挙動は変わらないため # url_prefix=""は必要ない


# 上記APIの完了時home.htmlの読み込み
@home_bp.route("/")  # ホームへのリクエスト
def home():
    videos = Video.query.filter(Video.created_at != None).all()
    years = sorted({video.created_at.year for video in videos}, reverse=True)
    return render_template("home.html", years=years)


# ECSのヘルスチェック用
@home_bp.route("/health")
def health_check():
    return jsonify({"status": "ok"}), 200
