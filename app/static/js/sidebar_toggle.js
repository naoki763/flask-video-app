document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("toggle-sidebar");
    const sidebarWrapper = document.querySelector(".sidebar-wrapper");

    if (toggleBtn && sidebarWrapper) {
        toggleBtn.addEventListener("click", function () {
            sidebarWrapper.classList.toggle("collapsed");  // ✅ これで開閉できる
        });
    }
});