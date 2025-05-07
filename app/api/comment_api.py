from flask import Blueprint, jsonify, request
from flask_login import current_user

from app.crud.comment import create_comment


comment_bp = Blueprint("comment", __name__, url_prefix="/comment")


# コメントを送信する
@comment_bp.route("/<int:video_id>", methods=["POST"])
def comment_handler(video_id):
    # year = request.args.get("year")

    # フォームなら request.form、JSONなら request.get_json()
    data = request.get_json()
    content = data.get("content")

    comment = create_comment(content, current_user.id, video_id)

    return jsonify(
        {
            "success": True,
            "content": comment.content,
            "username": current_user.username,
            "posted_at": comment.posted_at.strftime("%Y/%m/%d %H:%M"),
        }
    )
