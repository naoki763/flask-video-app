// upload.js

const dropArea = document.querySelector('.drag-drop-area');
const hiddenInput = document.getElementById('drag-drop-input');
const previewVideo = document.getElementById('preview');
const fileInput = document.getElementById('file');
const uploadBtn = document.getElementById('uploadBtn');

function isVideoFile(file) {
    return file && file.type.startsWith('video/');
}

function showError(message) {
    const errorDiv = document.getElementById("file-error");
    errorDiv.innerText = message;
    errorDiv.style.display = "block";
    previewVideo.hidden = true;
    fileInput.value = "";
    hiddenInput.value = "";
    uploadBtn.disabled = false;
}

// クリック選択対応
hiddenInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!isVideoFile(file)) {
        showError("動画ファイル以外はアップロードできません。");
        return;
    }
    fileInput.files = hiddenInput.files;
    previewVideo.src = URL.createObjectURL(file);
    previewVideo.hidden = false;
});

// 通常のファイル選択
fileInput.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (!isVideoFile(file)) {
        showError("動画ファイル以外はアップロードできません。");
        return;
    }
    const url = URL.createObjectURL(file);
    previewVideo.src = url;
    previewVideo.hidden = false;
});

// ドラッグオーバー時の見た目変更
dropArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropArea.classList.add('dragging');
});

dropArea.addEventListener('dragleave', () => {
    dropArea.classList.remove('dragging');
});

// ドロップ処理
dropArea.addEventListener('drop', (e) => {
    e.preventDefault();
    dropArea.classList.remove('dragging');

    const file = e.dataTransfer.files[0];
    if (!isVideoFile(file)) {
        showError("動画ファイル以外はアップロードできません。");
        return;
    }

    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    fileInput.files = dataTransfer.files;
    previewVideo.src = URL.createObjectURL(file);
    previewVideo.hidden = false;
});

// フォーム送信時のボタン無効化
document.querySelector('form').addEventListener('submit', function() {
    uploadBtn.disabled = true;
});
