from app.models.models import Comment, db


def create_comment(content, user_id, video_id):
    """コメントを新規作成する"""
    comment = Comment(
        content=content,
        user_id=user_id,
        video_id=video_id,
    )
    db.session.add(comment)
    db.session.commit()
    return comment
