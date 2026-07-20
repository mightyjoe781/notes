#!/usr/bin/env node
// The only piece that talks to Playwright/Chromium. Invoked once per build
// (not once per diagram) by scripts/render_excalidraw.py, with the full
// cache-miss batch for the whole run passed as a JSON file on argv[2].
//
// Launches one browser + one page, serves dist/ (the esbuild-bundled
// harness + offline fonts) over a local HTTP server, then loops the batch
// calling window.__excalidrawRenderToSvg (see src/harness-entry.js) once
// per block and writes each resulting SVG to disk.
//
// Usage: node render.mjs <batch.json>
//   batch.json: { "jobs": [ { key, outputPath, elements, appState, files, frameId }, ... ] }
// Prints a JSON array to stdout: [ { key, outputPath, ok, error? }, ... ]

import { chromium } from "playwright";
import { createServer } from "node:http";
import { readFile, writeFile, mkdir } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";

const here = path.dirname(fileURLToPath(import.meta.url));
const distDir = path.join(here, "dist");

const MIME = {
  ".html": "text/html",
  ".js": "text/javascript",
  ".woff2": "font/woff2",
  ".woff": "font/woff",
};

function serveDist() {
  const server = createServer(async (req, res) => {
    try {
      const url = new URL(req.url, "http://localhost");
      let rel = decodeURIComponent(url.pathname);
      if (rel === "/") rel = "/harness.html";
      const filePath = path.join(distDir, rel);
      if (!filePath.startsWith(distDir)) {
        res.writeHead(403);
        res.end();
        return;
      }
      const body = await readFile(filePath);
      const ext = path.extname(filePath);
      res.writeHead(200, { "Content-Type": MIME[ext] || "application/octet-stream" });
      res.end(body);
    } catch (err) {
      res.writeHead(404);
      res.end(String(err));
    }
  });
  return new Promise((resolve) => {
    server.listen(0, "127.0.0.1", () => resolve(server));
  });
}

async function main() {
  const batchPath = process.argv[2];
  if (!batchPath) {
    console.error("usage: node render.mjs <batch.json>");
    process.exit(1);
  }

  const batch = JSON.parse(await readFile(batchPath, "utf-8"));
  const jobs = batch.jobs || [];

  const results = [];

  if (jobs.length === 0) {
    console.log(JSON.stringify(results));
    return;
  }

  const server = await serveDist();
  const port = server.address().port;

  const browser = await chromium.launch();
  try {
    const page = await browser.newPage();
    await page.goto(`http://127.0.0.1:${port}/harness.html`);
    await page.waitForFunction(() => typeof window.__excalidrawRenderToSvg === "function");

    for (const job of jobs) {
      try {
        const svg = await page.evaluate(
          ({ sceneData, frameId }) => window.__excalidrawRenderToSvg(sceneData, frameId),
          {
            sceneData: {
              elements: job.elements,
              appState: job.appState,
              files: job.files,
            },
            frameId: job.frameId || null,
          },
        );
        await mkdir(path.dirname(job.outputPath), { recursive: true });
        await writeFile(job.outputPath, svg, "utf-8");
        results.push({ key: job.key, outputPath: job.outputPath, ok: true });
      } catch (err) {
        results.push({ key: job.key, outputPath: job.outputPath, ok: false, error: String(err) });
      }
    }
  } finally {
    await browser.close();
    server.close();
  }

  console.log(JSON.stringify(results));
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
