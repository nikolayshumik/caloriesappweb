/*var searchInput = document.getElementById('search-input');
var productItems = document.getElementsByClassName('product-item');

searchInput.addEventListener('input', function() {
  var query = searchInput.value.toLowerCase();
  for (var i = 0; i < productItems.length; i++) {
    var productItem = productItems[i];
    var productText = productItem.getElementsByTagName('text')[0].textContent.toLowerCase();
    if (productText.includes(query)) {
      productItem.style.display = 'block';
    } else {
      productItem.style.display = 'none';
    }
  }
});

  // Получение элементов и назначение обработчиков событий
  var createBtnshum = document.querySelector('#create-btnshum');
  var modalshum = document.querySelector('.modalshum');
  var closeBtnshum = document.querySelector('.closeX');
  
  createBtnshum.addEventListener('click', function() {
    modalshum.style.display = 'block';
  });
  
  closeBtnshum.addEventListener('click', function() {
    modalshum.style.display = 'none';
  });
  
  window.addEventListener('click', function(event) {
    if (event.target == modalshum) {
      modalshum.style.display = 'none';
    }
  });
  
  
  
      var modal = document.querySelector(".modal");
  
  function openModal2(productID) {
    var modalID = 'modal2_' + productID;
    document.getElementById(modalID).style.display = "block";
  }
  
  function closeModal2(productID) {
    var modalID = 'modal2_' + productID;
    document.getElementById(modalID).style.display = "none";
  }
  
      window.onclick = function (event) {
        if (event.target === modal) {
          closeModal();
        } else if (event.target.classList.contains('modal2')) {
          event.target.style.display = "none";
        }
      };
  
  
  
 // Получаем последнюю сохраненную позицию прокрутки
 var scrollPosition = sessionStorage.getItem('scrollPosition');

 // Восстанавливаем позицию прокрутки
 if (scrollPosition) {
     window.scrollTo(0, parseInt(scrollPosition));
 }

 // Сохраняем текущую позицию прокрутки перед обновлением страницы
 window.addEventListener('beforeunload', function () {
     sessionStorage.setItem('scrollPosition', window.scrollY);
 });

// Получаем кнопку прокрутки наверх
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
    window.scrollTo(0, 0);
});
*/
var createBtnshum = document.querySelector('#create-btnshum');

createBtnshum.addEventListener('click', function() {
    modalshum.style.display = 'block';
  });