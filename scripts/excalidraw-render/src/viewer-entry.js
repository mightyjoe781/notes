// Live viewer entry point, bundled by build.mjs into dist/viewer.js and
// copied to docs/assets/papers/ so mkdocs serves it -- but only ever loaded
// by overrides/papers.html (a per-page `template:` used solely by pages
// under docs/papers/). No other page on the site references this bundle.
//
// Unlike harness-entry.js (which drives Excalidraw's *static* export
// utilities from Node/Playwright to produce an SVG once at build time),
// this mounts the real <Excalidraw> React component live in the reader's
// own browser, in read-only viewMode: real pan/zoom/click-through, not a
// flattened image.
//
// EXCALIDRAW_ASSET_PATH must be set before the package is imported (same
// requirement as harness-entry.js) -- fonts are fetched relative to it.
// build.mjs copies the package's own font files to docs/assets/papers/fonts,
// so this must match that destination.
import React from "react";
import { createRoot } from "react-dom/client";
import { Excalidraw } from "@excalidraw/excalidraw";
import "@excalidraw/excalidraw/index.css";

window.EXCALIDRAW_ASSET_PATH = "/assets/papers/";

const MOUNT_ID = "papers-viewer";
let root = null;

async function mount() {
  const el = document.getElementById(MOUNT_ID);
  if (!el) return; // not a papers page (shouldn't happen, this bundle only loads there)

  const sceneUrl = el.dataset.sceneUrl;
  el.textContent = "Loading scene...";

  let scene;
  try {
    const res = await fetch(sceneUrl);
    if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
    scene = await res.json();
  } catch (err) {
    el.textContent = `Failed to load scene: ${err.message}`;
    return;
  }

  el.textContent = "";
  if (!root) root = createRoot(el);
  root.render(
    React.createElement(Excalidraw, {
      viewModeEnabled: true,
      initialData: {
        elements: scene.elements,
        appState: scene.appState,
        files: scene.files,
      },
    }),
  );
}

// mkdocs-material's `navigation.instant` swaps page <body> content via
// fetch rather than a full page load, so a plain DOMContentLoaded listener
// only ever fires once and misses every subsequent in-site navigation into
// a papers page. document$ is Material's own RxJS observable, documented
// for exactly this: it emits once per real page AND once per instant-nav
// swap, so this covers both a hard load and clicking in from another page.
if (window.document$ && typeof window.document$.subscribe === "function") {
  window.document$.subscribe(mount);
} else {
  document.addEventListener("DOMContentLoaded", mount);
}
