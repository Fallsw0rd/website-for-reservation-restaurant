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
