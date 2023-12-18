document.addEventListener('DOMContentLoaded', function() {
    const currentPage = window.location.pathname + window.location.search;
    const navLinks = document.querySelectorAll('.nav-item');

    navLinks.forEach(function(link) {
        const linkUrl = link.getAttribute('href');

        if (currentPage.startsWith(linkUrl)) {
            link.classList.add('active');
        }
    });
});

document.getElementById("mobile-btn").addEventListener("click", function() {
        let mobileMenu = document.getElementById("mobile");
        // Переключаем стиль дисплея между "flex" и "none"
        mobileMenu.style.display = (mobileMenu.style.display === "flex") ? "none" : "flex";
    });
