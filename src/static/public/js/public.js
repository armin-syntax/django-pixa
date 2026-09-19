document.addEventListener("click", (event) => {
  const button = event.target.closest(".card-menu-button");
  const openMenus = document.querySelectorAll(".card-menu.open");

  if (button) {
    const menu = button.closest(".card-menu");
    const isOpen = menu.classList.contains("open");

    openMenus.forEach((item) => {
      item.classList.remove("open");
      item.querySelector(".card-menu-button")?.setAttribute("aria-expanded", "false");
    });

    if (!isOpen) {
      menu.classList.add("open");
      button.setAttribute("aria-expanded", "true");
    }

    return;
  }

  if (!event.target.closest(".card-menu")) {
    openMenus.forEach((menu) => {
      menu.classList.remove("open");
      menu.querySelector(".card-menu-button")?.setAttribute("aria-expanded", "false");
    });
  }
});