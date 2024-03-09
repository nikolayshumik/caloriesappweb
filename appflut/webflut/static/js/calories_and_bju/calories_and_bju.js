document.querySelectorAll('.clickable').forEach(item => {
    item.addEventListener('click', event => {
        event.target.parentElement.classList.toggle('active');
    });
})