const html = document.documentElement;
const saved = localStorage.getItem("theme") || "light";
html.setAttribute("data-theme", saved);
updateIcons(saved);

function toggleTheme() {
  const current = html.getAttribute("data-theme");
  const next = current === "dark" ? "light" : "dark";
  html.setAttribute("data-theme", next);
  localStorage.setItem("theme", next);
  updateIcons(next);
}

function updateIcons(theme) {
  document
    .getElementById("theme-icon-dark")
    .classList.toggle("hidden", theme === "dark");
  document
    .getElementById("theme-icon-light")
    .classList.toggle("hidden", theme === "light");
}
