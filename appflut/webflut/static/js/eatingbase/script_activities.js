var scrollTopButton = document.getElementById('scrollTopButton');

// Отслеживаем событие прокрутки страницы
window.addEventListener('scroll', function () {
    // Если прокрутка больше определенной высоты, показываем кнопку
    if (window.scrollY > 400) {
        scrollTopButton.classList.add('show');
    } else {
        scrollTopButton.classList.remove('show');
    }
});

// Отслеживаем событие клика на кнопке
scrollTopButton.addEventListener('click', function () {
    // Прокручиваем страницу наверх
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
});

var searchInput = document.getElementById('search-input');

searchInput.addEventListener('input', debounce(function () {
    var query = searchInput.value.toLowerCase();
    var results = document.getElementsByClassName('product-item');
    
    for (var i = 0; i < results.length; i++) {
        var result = results[i];
        var text = result.querySelector('.text').textContent.toLowerCase();
        
        if (text.includes(query)) {
            result.style.display = 'block';
        } else {
            result.style.display = 'none';
        }
    }
}, 300));

function debounce(func, delay) {
    var timer = null;
    
    return function () {
        clearTimeout(timer);
        timer = setTimeout(func, delay);
    };
}

var scrollPosition = sessionStorage.getItem('scrollPosition');

// Восстанавливаем позицию прокрутки
if (scrollPosition) {
    window.scrollTo({
        top: parseInt(scrollPosition),
        behavior: "smooth"
    });
}

// Сохраняем текущую позицию прокрутки перед обновлением страницы
window.addEventListener('beforeunload', function () {
    sessionStorage.setItem('scrollPosition', window.scrollY);
});

function openModal(id) {
    document.querySelector(`#modal-${id}`).style.display = "block";
    document.querySelector('#add-button').style.display = "none";
}

function closeModal(id) {
    document.querySelector('#add-button').style.display = "block";
    document.querySelector(`#modal-${id}`).style.display = "none";
}

window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = "none";
    }
};
