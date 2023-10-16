
//datetime
var currentDateElement = document.getElementById("currentDate");

function getCurrentDate() {
  var currentDate = new Date();
  var options = { weekday: 'long', day: 'numeric', month: 'long' };
  var formattedDate = currentDate.toLocaleDateString("ru-RU", options);
  return formattedDate;
}

currentDateElement.textContent = getCurrentDate();



//modal window
    var modal = document.getElementById("modal");

function openModal() {
  modal.style.display = "block";
}

function closeModal() {
  modal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target === modal) {
    closeModal();
  }
};

