var katexConfig = {
  delimiters: [
    { left: "$$", right: "$$", display: true },
    { left: "$",  right: "$",  display: false },
    { left: "\\(", right: "\\)", display: false },
    { left: "\\[", right: "\\]", display: true },
  ],
  throwOnError: false,
  macros: {
    "\\tag": "\\notag",
  },
};

function renderMath() {
  if (typeof renderMathInElement !== "undefined") {
    renderMathInElement(document.body, katexConfig);
  }
}

// Fires after all async scripts (including KaTeX CDN) have loaded
window.addEventListener("load", renderMath);

// Fires on each instant navigation (KaTeX is already loaded by this point)
if (typeof document$ !== "undefined") {
  document$.subscribe(renderMath);
}
