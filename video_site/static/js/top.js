document.addEventListener("DOMContentLoaded", function () {
    var menuBtn = document.getElementById("menu-btn-check");
    var menuContent = document.querySelector(".menu-content");

    menuBtn.addEventListener("mouseover", function () {
        menuContent.style.display = "block"; // メニューを表示
    });

    menuBtn.addEventListener("mouseout", function () {
        menuContent.style.display = "none"; // メニューを非表示
    });
});