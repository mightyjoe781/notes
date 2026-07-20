// One-time (or "when the harness source / Excalidraw version changes")
// bundle step. Run via `npm run build`. Produces dist/, which render.mjs
// serves as a static site for Playwright to navigate to -- fully offline,
// no unpkg/CDN fetches at build time.
import { build } from "esbuild";
import { cpSync, mkdirSync, copyFileSync, rmSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const here = path.dirname(fileURLToPath(import.meta.url));
const distDir = path.join(here, "dist");

rmSync(distDir, { recursive: true, force: true });
mkdirSync(distDir, { recursive: true });

await build({
  entryPoints: [path.join(here, "src", "harness-entry.js")],
  bundle: true,
  format: "iife",
  platform: "browser",
  outfile: path.join(distDir, "harness.js"),
  loader: { ".woff2": "text", ".woff": "text" }, // unused by our code path, just prevents esbuild erroring if pulled in
  define: { "process.env.NODE_ENV": '"production"' },
  logLevel: "info",
});

copyFileSync(path.join(here, "harness.html"), path.join(distDir, "harness.html"));

// @excalidraw/excalidraw resolves fonts at runtime relative to
// window.EXCALIDRAW_ASSET_PATH (set to "/" in harness-entry.js), fetching
// e.g. "/fonts/Virgil/Virgil-Regular.woff2". Copying the package's own
// prebuilt font files here (instead of re-deriving/reimplementing font
// loading) is what keeps text layout correct and the whole render offline.
cpSync(
  path.join(here, "node_modules", "@excalidraw", "excalidraw", "dist", "prod", "fonts"),
  path.join(distDir, "fonts"),
  { recursive: true },
);

console.log(`Built harness -> ${path.relative(process.cwd(), distDir)}/`);
