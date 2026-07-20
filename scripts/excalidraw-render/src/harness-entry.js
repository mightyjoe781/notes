// Harness entry point, bundled by build.mjs into dist/harness.js and loaded
// by render.mjs (via Playwright) in dist/harness.html.
//
// Excalidraw scene JSON isn't self-describing: it only becomes a real
// diagram once run through Excalidraw's own renderer (RoughJS sketchy
// strokes + real font-metrics text layout). This file imports the actual
// @excalidraw/excalidraw package -- not a reimplementation -- and exposes
// its exportToSvg/restore utilities on `window` so render.mjs can drive
// them from Node via Playwright's page.evaluate().
//
// EXCALIDRAW_ASSET_PATH must be set before any Excalidraw code runs: it's
// the override the package checks (instead of defaulting to the unpkg CDN)
// to resolve font files, so the render stays fully offline. build.mjs
// copies dist/prod/fonts next to this bundle so "/" (server root) resolves
// correctly.
import { exportToSvg, restore } from "@excalidraw/excalidraw";

window.EXCALIDRAW_ASSET_PATH = "/";

/**
 * Render one block (a filtered elements array + appState + files) to an SVG
 * string. Mirrors what scripts/render_excalidraw.py hands to render.mjs
 * per cache-miss.
 *
 * @param {object} sceneData - { elements, appState, files }
 * @param {string|null} frameId - id of the frame element (already present in
 *   sceneData.elements) to crop/export to, or null for the whole-scene
 *   "default" block.
 */
window.__excalidrawRenderToSvg = async function (sceneData, frameId) {
  const restored = restore(
    {
      elements: sceneData.elements,
      appState: sceneData.appState,
      files: sceneData.files,
    },
    null,
    null,
  );

  const exportingFrame = frameId
    ? restored.elements.find((el) => el.id === frameId && el.type === "frame")
    : undefined;

  const svg = await exportToSvg({
    elements: restored.elements,
    appState: {
      ...restored.appState,
      exportBackground: true,
    },
    files: restored.files,
    exportPadding: 16,
    exportingFrame,
  });

  return svg.outerHTML;
};
