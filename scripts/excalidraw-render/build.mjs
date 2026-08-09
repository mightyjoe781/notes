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
// scripts/excalidraw-render/ -> repo root -> docs/assets/papers/. This is
// the ONLY output of this script that mkdocs actually publishes (dist/ is
// consumed solely by the headless Playwright harness below, never served).
const papersAssetsDir = path.join(here, "..", "..", "docs", "assets", "papers");

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

// Live, read-only viewer bundle for docs/papers/ pages (see
// overrides/papers.html). Same toolchain as the harness build above, a
// separate entry point -- this one runs in a real reader's browser, not
// headless Chromium.
rmSync(papersAssetsDir, { recursive: true, force: true });
mkdirSync(papersAssetsDir, { recursive: true });

await build({
  entryPoints: [path.join(here, "src", "viewer-entry.js")],
  bundle: true,
  format: "iife",
  platform: "browser",
  outfile: path.join(papersAssetsDir, "viewer.js"),
  // The package's "./index.css" export only declares "development" /
  // "production" conditions (no "default"), so esbuild needs to be told
  // which one to pick -- otherwise it can't resolve the import at all.
  conditions: ["production"],
  loader: { ".woff2": "text", ".woff": "text" },
  define: { "process.env.NODE_ENV": '"production"' },
  // Unlike the harness (built once, run through headless Chromium locally
  // during a build and never shipped), this bundle is downloaded by every
  // reader's real browser -- minify it.
  minify: true,
  logLevel: "info",
});

// esbuild extracts CSS pulled in via `import "@excalidraw/excalidraw/index.css"`
// into a sibling dist/viewer.css automatically -- nothing else to do here.

// Same font-resolution requirement as the harness build, but the base URL
// here is window.EXCALIDRAW_ASSET_PATH = "/assets/papers/" (set in
// viewer-entry.js) to match where mkdocs actually serves this directory.
cpSync(
  path.join(here, "node_modules", "@excalidraw", "excalidraw", "dist", "prod", "fonts"),
  path.join(papersAssetsDir, "fonts"),
  { recursive: true },
);

console.log(`Built papers viewer -> ${path.relative(process.cwd(), papersAssetsDir)}/`);
