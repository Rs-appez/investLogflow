document.addEventListener("DOMContentLoaded", function () {
  document.body.addEventListener("htmx:afterSwap", (e) => {
    if (e.target.id === "stock-buy-modal-container") {
      document.getElementById("stock-buy-modal").showModal();
    }
  });
});
