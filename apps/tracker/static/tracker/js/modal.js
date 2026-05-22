document.addEventListener("DOMContentLoaded", function () {
  document.body.addEventListener("htmx:afterSwap", (e) => {
    if (e.target.id === "stock-buy-modal") {
      document.getElementById("stock-buy-modal").showModal();
    }
  });
});
