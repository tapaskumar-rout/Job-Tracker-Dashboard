document.addEventListener("DOMContentLoaded", () =>{
  const toggle = document.getElementById("themeToggle");

  //Apply saved theme
  const savedTheme = localStorage.getItem("theme") || "light";
  document.body.setAttribute("data-theme", savedTheme);

  if (toggle) {
    toggle.innerHTML = 
    savedTheme === "dark"
      ? '<i class="bi bi-sun-fill"></i>'
      :'<i class="bi bi-moon-fill"></i>';

    toggle.addEventListener("click", () => {

      const current = document.body.getAttribute("data-theme");
      const next = current === "dark" ? "light" : "dark";
      document.body.setAttribute("data-theme", next);
      localStorage.setItem("theme", next);

      toggle.innerHTML =
         next === "dark"
         ? '<i class="bi bi-sun-fill"></i>'
         : '<i class="bi bi-moon-fill"></i>';
    }); 
  }
});