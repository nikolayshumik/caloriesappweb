window.onload = function() {
    var searchInput = document.getElementById("search-input");
    var productItems = document.getElementsByClassName("product-item");
    var modal = document.querySelector(".modal");
    var scrollTopButton = document.getElementById("scrollTopButton");
    var scrollPosition = sessionStorage.getItem("scrollPosition");
    var createBtnshum = document.querySelector("#create-btnshum");
    var modalshum = document.querySelector(".modalshum");
    var closeBtnshum = document.querySelector(".closeX");
  
    searchInput.addEventListener("input", function() {
      var query = searchInput.value.toLowerCase();
      for (var i = 0; i < productItems.length; i++) {
        var productItem = productItems[i];
        var productText = productItem
          .getElementsByTagName("text")[0]
          .textContent.toLowerCase();
        if (productText.includes(query)) {
          productItem.style.display = "block";
        } else {
          productItem.style.display = "none";
        }
      }
    });
  
    createBtnshum.addEventListener("click", function() {
      modalshum.style.display = "block";
    });
  
    closeBtnshum.addEventListener("click", function() {
      modalshum.style.display = "none";
    });
  
    window.addEventListener("click", function(event) {
      if (event.target == modalshum) {
        modalshum.style.display = "none";
      } else if (event.target === modal) {
        closeModal();
      } else if (event.target.classList.contains("modal2")) {
        event.target.style.display = "none";
      }
    });
  
    function openModal2(productID) {
      var modalID = "modal2_" + productID;
      document.getElementById(modalID).style.display = "block";
    }
  
    function closeModal2(productID) {
      var modalID = "modal2_" + productID;
      document.getElementById(modalID).style.display = "none";
    }
  
    if (scrollPosition) {
      window.scrollTo(0, parseInt(scrollPosition));
    }
  
    window.addEventListener("beforeunload", function() {
      sessionStorage.setItem("scrollPosition", window.scrollY);
    });
  
    window.addEventListener("scroll", function() {
      if (window.scrollY > 400) {
        scrollTopButton.classList.add("show");
      } else {
        scrollTopButton.classList.remove("show");
      }
    });
  
    scrollTopButton.addEventListener("click", function() {
      window.scrollTo(0, 0);
    });
  };