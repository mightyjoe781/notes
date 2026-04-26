function renderMath() {
  renderMathInElement(document.body, {
    delimiters: [
      { left: "$$", right: "$$", display: true },
      { left: "$",  right: "$",  display: false },
      { left: "\\(", right: "\\)", display: false },
      { left: "\\[", right: "\\]", display: true },
    ],
    throwOnError: false,
  });
}

if (typeof document$ !== "undefined") {
  document$.subscribe(renderMath);
} else {
  document.addEventListener("DOMContentLoaded", renderMath);
}
