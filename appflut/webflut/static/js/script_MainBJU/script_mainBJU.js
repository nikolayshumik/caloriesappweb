document.querySelectorAll('.clickable').forEach(item => {
    item.addEventListener('click', event => {
        event.target.parentElement.classList.toggle('active');
    });
})
// Сохраняем состояние класса "active" перед обновлением страницы
window.addEventListener('beforeunload', function () {
    var eatings = document.getElementsByClassName('eatings');
    for (var i = 0; i < eatings.length; i++) {
        var eating = eatings[i];
        if (eating.classList.contains('active')) {
            localStorage.setItem('eatings-' + i, 'active');
        } else {
            localStorage.removeItem('eatings-' + i);
        }
    }
});

// Восстанавливаем состояние класса "active" после обновления страницы
window.addEventListener('load', function () {
    var eatings = document.getElementsByClassName('eatings');
    for (var i = 0; i < eatings.length; i++) {
        var eating = eatings[i];
        var isActive = localStorage.getItem('eatings-' + i);
        if (isActive === 'active') {
            eating.classList.add('active');
        } else {
            eating.classList.remove('active');
        }
    }
});
 // Сохраняем позицию прокрутки перед обновлением страницы
 window.addEventListener('beforeunload', function() {
    localStorage.setItem('scrollPosition', window.pageYOffset);
});

// Восстанавливаем позицию прокрутки после обновления страницы
window.addEventListener('load', function() {
    var scrollPosition = localStorage.getItem('scrollPosition');
    if (scrollPosition) {
        window.scrollTo(0, scrollPosition);
        localStorage.removeItem('scrollPosition');
    }
});