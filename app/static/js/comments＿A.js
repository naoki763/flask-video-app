document.addEventListener("DOMContentLoaded", function () {
    var commentForm = document.getElementById("comment-form");
    var commentInput = document.getElementById("comment");
    var videoIdElement = document.getElementById("video_id");

    // ✅ video_id の要素が存在するかチェック
    if (!videoIdElement) {
        console.error("エラー: video_id が見つかりません");
        return;
    }

    var videoId = videoIdElement.value;
    console.log("デバッグ: videoId =", videoId);  // ✅ デバッグ用ログ

    // ✅ コメントを取得して表示する関数（初回ロード時には呼ばない）
    function fetchComments() {
        fetch(`/comment/list/${videoId}`)
            .then(response => response.json())
            .then(data => {
                var commentList = document.getElementById("comment-list");
                commentList.innerHTML = ""; // 既存のコメントをクリアして更新

                data.forEach(comment => {
                    var newComment = document.createElement("li");
                    newComment.innerHTML = `<strong>${comment.username}</strong>: ${comment.comment}  
                                            <small>(${comment.timestamp})</small>`;
                    commentList.appendChild(newComment);
                });
            })
            .catch(error => console.error("コメントの取得エラー:", error));
    }

    if (commentForm) {
        commentForm.addEventListener("submit", function (event) {
            event.preventDefault();

            var commentText = commentInput.value.trim();
            if (!commentText) {
                alert("コメントを入力してください！");
                return;
            }

            console.log("送信データ:", { video_id: videoId, comment: commentText });  // ✅ デバッグ用

            fetch("/comment/post", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ video_id: videoId, comment: commentText }),
            })
            .then(response => {
                console.log("レスポンスステータス:", response.status);
                if (!response.ok) {
                    throw new Error("サーバーエラー: " + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                if (data.status === "success") {
                    fetchComments();  // ✅ コメント投稿完了後にのみ取得
                    commentInput.value = ""; // コメント入力欄をクリア
                } else {
                    alert("コメントの投稿に失敗しました: " + data.message);
                }
            })
            .catch(error => console.error("Error:", error));
        });
    }
});