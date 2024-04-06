let scrollTopButton = document.getElementById("scrollTopButton");
let searchInput = document.getElementById("search-input");
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

searchInput.addEventListener(
  "input",
  debounce(function () {
    let query = searchInput.value;
    if (query.length > 0) {
      let results = document.getElementsByClassName("activities-item");
      for (let i = 0; i < results.length; i++) {
        let result = results[i];
        let text = result.querySelector("text").textContent.toLowerCase();
        if (text.includes(query.toLowerCase())) {
          result.style.display = "block";
        } else {
          result.style.display = "none";
        }
      }
    } else {
      let results = document.getElementsByClassName("activities-item");
      for (let i = 0; i < results.length; i++) {
        let result = results[i];
        result.style.display = "block";
      }
    }
  }, 300)
);

function debounce(func, delay) {
  let timer = null;
  return function () {
    clearTimeout(timer);
    timer = setTimeout(func, delay);
  };
}

function openModal(id) {
  document.querySelector(`#modal-${id}`).style.display = "flex";
  document.querySelector("#add-button").style.display = "none";
}

function closeModal(id) {
  document.querySelector("#add-button").style.display = "flex";
  document.querySelector(`#modal-${id}`).style.display = "none";
}

window.onclick = function (event) {
  if (event.target.classList.contains("modal")) {
    event.target.style.display = "none";
  }
};
