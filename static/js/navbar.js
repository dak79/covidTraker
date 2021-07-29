// Toggle menu

document.addEventListener('DOMContentLoaded', () => {
    const hamburger = document.querySelector('.hamburger')
    const hamburgerOpen = document.querySelector('.hamburger-open');
    const hamburgerClose = document.querySelector('.hamburger-close');
    const navMenu = document.querySelector('.nav-menu');

    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active')
        hamburgerOpen.classList.toggle('active');
        hamburgerClose.classList.toggle('active');
        navMenu.classList.toggle('active');
    });
})