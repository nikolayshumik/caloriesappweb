let searchInput = document.getElementById("search-input");
let productItems = document.getElementsByClassName("product-item");
let modal = document.querySelector(".modal");
let createMyProduct = document.querySelector("#create-my-product");
let modalshum = document.querySelector(".modalCreacteProduct");
let closeProduct = document.querySelector(".closeX");
let scrollTopButton = document.getElementById("scrollTopButton");

//Алгоритм поиска
searchInput.addEventListener("input", function () {
  let query = searchInput.value.toLowerCase();
  for (let i = 0; i < productItems.length; i++) {
    let productItem = productItems[i];
    let productText = productItem
      .getElementsByTagName("text")[0]
      .textContent.toLowerCase();
    if (productText.includes(query)) {
      productItem.style.display = "block";
    } else {
      productItem.style.display = "none";
    }
  }
});
////Алгоритм поиска///

createMyProduct.addEventListener("click", function () {
  modalshum.style.display = "block";
});

closeProduct.addEventListener("click", function () {
  modalshum.style.display = "none";
});

//Логика работы модального окна
window.addEventListener("click", function (event) {
  if (event.target == modalshum) {
    modalshum.style.display = "none";
  } else if (event.target === modal) {
    closeModal();
  } else if (event.target.classList.contains("modal2")) {
    event.target.style.display = "none";
  }
});
/////Логика работы модального окна

function openModal2(productID) {
  let modalID = "modal2_" + productID;
  document.getElementById(modalID).style.display = "block";
}

function closeModal2(productID) {
  let modalID = "modal2_" + productID;
  document.getElementById(modalID).style.display = "none";
}

//Скролл
window.addEventListener("scroll", function () {
  if (window.scrollY > 300) {
    scrollTopButton.classList.add("show");
    scrollTopButton.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  } else {
    scrollTopButton.classList.remove("show");
  }
});
