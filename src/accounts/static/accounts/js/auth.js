const codeInput = document.querySelector(".code-input");

if (codeInput) {
  codeInput.addEventListener("input", () => {
    codeInput.value = codeInput.value.replace(/\D/g, "").slice(0, 6);
  });
}