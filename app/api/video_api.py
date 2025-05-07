from datetime import datetime

from flask import Blueprint, redirect, render_template, url_for

from app.crud.video import (
    create_video,
    delete_video_by_id,
    get_all_videos,
    get_video_by_id,
    get_video_with_comments,
    get_videos_by_year,
    get_years_available,
    group_videos_by_month,
)
from app.schemas.video import VideoUploadForm
from app.service.video_service import delete_s3_for_video, upload_s3_for_video


video_bp = Blueprint("video", __name__, url_prefix="/video")


# 動画とコメントを表示
@video_bp.route("/<int:video_id>", methods=["GET"])
def show_video_with_comments(video_id):
    video = get_video_with_comments(video_id)
    return render_template("select_movie.html", video=video, comments=video.comments)


# 年別、月別の動画リストを表示
@video_bp.route("/list/<int:year>", methods=["GET"])
def video_list_by_year(year):
    videos = get_videos_by_year(year)
    videos_by_month = group_videos_by_month(videos)
    years = get_years_available()
    return render_template(
        "select_after.html", year=year, years=years, videos_by_month=videos_by_month
    )


# アップロード画面を表示
@video_bp.route("/upload", methods=["GET"])
def upload_form():
    videos = get_all_videos()
    form = VideoUploadForm()
    return render_template("upload.html", videos=videos, form=form)


# 動画アップロードのエンドポイント
@video_bp.route("/upload", methods=["POST"])
def upload_video():
    # リクエストの検証
    form = VideoUploadForm()
    if not form.validate_on_submit():
        return redirect(url_for("video.upload_form"))

    file = form.file.data
    title = form.title.data or "Untitled"  # タイトルがない場合 "Untitled"

    # s3バケットへファイルを保存
    upload_result = upload_s3_for_video(file, title)

    # DB保存
    create_video(upload_result)

    # 保存する動画の撮影日を取得
    year = (
        upload_result.created_at.year
        if upload_result.created_at
        else datetime.now().year
    )

    return redirect(url_for("video.video_list_by_year", year=year))


@video_bp.route("/delete/<int:video_id>", methods=["POST"])
def delete_video(video_id):
    video = get_video_by_id(video_id)
    # 動画のURL
    video_url = video.url
    # サムネイルのURL
    thumbnail_url = video.thumbnail_url

    year = video.created_at.year if video.created_at else datetime.now().year

    delete_s3_for_video(video_url, thumbnail_url)

    delete_video_by_id(video_id)

    return redirect(url_for("video.video_list_by_year", year=year))


# 動画アップロードのエンドポイント
# @video_bp.route("/upload", methods=["POST"])
# def upload_video():
#     if "file" not in request.files:
#         return jsonify({"error": "No file part"}), 400

#     file = request.files["file"]
#     title = request.form.get("title", "Untitled")  # タイトルがない場合 "Untitled"

#     if file.filename == "":
#         return jsonify({"error": "No selected file"}), 400

#     # 既存の `user_id` があるか確認（方法②）
#     existing_video = Video.query.filter_by(url=file.filename).first()
#     if existing_video:
#         return jsonify({"error": "File already exists"}), 400

#     unique_filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"

#     # ---temp-----
#     # サムネイル生成（ローカルに一時保存）
#     # サムネイルの一時的なファイル保存場所を作成
#     temp_video_path = f"/tmp/{unique_filename}"
#     # それを一度ローカル保存が必要（ffmpeg用）、なのでここで一時的に動画自体をこのファイルに一時的に保存している
#     file.save(temp_video_path)  # 一度ローカル保存が必要（ffmpeg用）
#     # ---temp-----

#     print(f"✅ ファイル保存成功: {temp_video_path}")
#     print(f"📦 実サイズ: {os.path.getsize(temp_video_path)} bytes")
#     # サイズ 0 だったら処理ストップ
#     if os.path.getsize(temp_video_path) == 0:
#         return jsonify(
#             {"error": "アップロードされたファイルが無効です（サイズ0）"}
#         ), 400

#     # ---ffprobe-----
#     # ここで撮影日時を取得（ffprobe経由）
#     from app.service.thumbnail_generator import get_creation_time

#     creation_time_str = get_creation_time(temp_video_path)
#     created_at = None
#     if creation_time_str:
#         try:
#             created_at = datetime.fromisoformat(
#                 creation_time_str.replace("Z", "+00:00")
#             )
#         except Exception as e:
#             print(f"⛔ created_at の変換に失敗: {e}")
#             created_at = datetime.now()
#     # ---ffprobe-----

#     # ---動画保存---
#     # S3への動画のURLを生成
#     file_url = generate_s3_url(unique_filename)

#     # S3に動画をアップロード
#     upload_s3(file, unique_filename)
#     # ---動画保存---

#     # ---サムネイル生成---
#     # アップロードしたS3のパスを参照したものに拡張子を .mp4 → .jpg に置き換えS3上のサムネイルのパスを作成
#     thumbnail_filename = unique_filename.rsplit(".", 1)[0] + ".jpg"
#     print(thumbnail_filename)
#     # S３に上げた動画のパスを/tmp/を付けて一時的にサムネイルを置くパスを作成している
#     thumbnail_path = f"/tmp/{thumbnail_filename}"
#     # ここでサムネイルを作る generate_thumbnai別途ファイルね
#     generate_thumbnail(temp_video_path, thumbnail_path)

#     # サムネイルをS3にアップロード
#     with open(thumbnail_path, "rb") as thumb_file:
#         upload_s3(thumb_file, f"thumbnails/{thumbnail_filename}")
#     # だから、ここでS３用のサムネイルのパスを作成完了
#     thumbnail_url = generate_s3_url(f"thumbnails/{thumbnail_filename}")
#     # ---サムネイル生成---

#     # ---DB保存---
#     # **DB に動画情報を保存**
#     new_video = Video(
#         user_id=current_user.id,
#         title=title,
#         url=file_url,
#         thumbnail_url=thumbnail_url,
#         created_at=created_at,
#     )
#     db.session.add(new_video)
#     db.session.commit()
#     # ---DB保存---
#     year = created_at.year if created_at else datetime.now().year

#     # フロントエンドが message & url を受け取って ページをリロードせずに動画リストを更新
#     return redirect(url_for("video.video_list_by_year", year=year))


# @video_bp.route("/delete/<int:video_id>", methods=["POST"])
# def delete_video(
#     video_id,
# ):  # video.id：これは データベースのVideoテーブルの主キー（UUID）を取ってくる
#     video = Video.query.get_or_404(video_id)
#     # 動画のURL
#     url = video.url
#     # サムネイルのURL
#     thumbnail_url = video.thumbnail_url

#     # 動画とサムネイルのファイルkeyを取得
#     video_key = extract_key_from_url(url)
#     thumbnail_key = extract_key_from_url(thumbnail_url)

#     try:
#         ## S3から動画とサムネイルを削除
#         delete_s3(video_key)
#         delete_s3(thumbnail_key)
#         print(f"[S3] Deleted: {video_key}: {thumbnail_key}")
#     except Exception as e:
#         print(f"[S3] Error deleting {video_key}:{thumbnail_key}::{e}")

#     db.session.delete(video)
#     db.session.commit()

#     year = video.created_at.year if video.created_at else datetime.now().year

#     return redirect(url_for("video.video_list_by_year", year=year))

# @video_bp.route("/delete/<int:video_id>", methods=["POST"])
# def delete_video(
#     video_id,
# ):  # video.id：これは データベースのVideoテーブルの主キー（UUID）を取ってくる
#     video = Video.query.get_or_404(video_id)
#     # 動画のURL
#     url = video.url
#     # サムネイルのURL
#     thumbnail_url = video.thumbnail_url

#     # 動画とサムネイルのファイルkeyを取得
#     video_key = extract_key_from_url(url)
#     thumbnail_key = extract_key_from_url(thumbnail_url)

#     try:
#         ## S3から動画とサムネイルを削除
#         delete_s3(video_key)
#         delete_s3(thumbnail_key)
#         print(f"[S3] Deleted: {video_key}: {thumbnail_key}")
#     except Exception as e:
#         print(f"[S3] Error deleting {video_key}:{thumbnail_key}::{e}")

#     db.session.delete(video)
#     db.session.commit()

#     year = video.created_at.year if video.created_at else datetime.now().year

#     return redirect(url_for("video.video_list_by_year", year=year))
