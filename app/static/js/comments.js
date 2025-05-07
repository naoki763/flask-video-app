document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("comment-form");
    const input = document.getElementById("comment-input");
    const commentList = document.getElementById("comment-list");

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const content = input.value.trim();
        if (!content) return;

        const postUrl = form.dataset.postUrl;

        fetch(postUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ content: content })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const newComment = document.createElement("div");
                newComment.classList.add("comment", "border", "rounded", "p-2", "mb-2"); // Bootstrapのクラスを適用
                newComment.innerHTML = `
                    <div class="username fw-bold">
                        ${data.username}（${data.posted_at}）
                    </div>
                    <div class="text">${data.content}</div>
                `;
                commentList.appendChild(newComment);
                input.value = "";
            } else {
                alert("投稿失敗しました");
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
    });
});
