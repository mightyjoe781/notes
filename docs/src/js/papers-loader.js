// Site-wide (loaded on every page via extra_javascript) but tiny -- this is
// NOT the ~8MB Excalidraw viewer bundle, just a conditional loader for it.
//
// Why this can't just be a <script> tag in overrides/papers.html: with
// navigation.instant enabled, mkdocs-material swaps the page by fetching
// and replacing <body> content, it does not inject a per-template <script
// src> that wasn't already present in the document. A reader who arrives
// at a papers page via an in-site link (not a hard reload) would see the
// mount div appear with no bundle ever having loaded to fill it. This
// loader is present on every page precisely so it's already there to react
// to that swap, and only ever does anything when it actually finds the
// papers mount point -- everywhere else it's a no-op.
function ensurePapersViewer() {
  if (!document.getElementById("papers-viewer")) return;
  if (document.querySelector('script[src*="assets/papers/viewer.js"]')) return; // already injected once

  // Absolute from site root, not relative to the current page -- this
  // script runs at whatever depth the current page is at (e.g.
  // /papers/test-paper/), and a relative path would resolve underneath it.
  var css = document.createElement("link");
  css.rel = "stylesheet";
  css.href = "/assets/papers/viewer.css";
  document.head.appendChild(css);

  var script = document.createElement("script");
  script.src = "/assets/papers/viewer.js";
  document.head.appendChild(script);
}

if (typeof document$ !== "undefined") {
  document$.subscribe(ensurePapersViewer);
} else {
  document.addEventListener("DOMContentLoaded", ensurePapersViewer);
}
