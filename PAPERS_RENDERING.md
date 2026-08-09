# Papers: live interactive Excalidraw viewer

How annotated research papers become a live, read-only, pan/zoom/click
Excalidraw canvas at `/papers/`, instead of a flattened image. Builds on
top of the pipeline described in `EXCALIDRAW_RENDERING.md` — read that
first if you haven't; this doc only covers what's different for papers.

## The problem this solves

The existing Excalidraw pipeline flattens every scene to a static SVG at
build time. That's the right call for diagrams embedded in regular notes,
but it throws away exactly what matters for an annotated paper: following
an arrow across a dense page, panning into a citation, zooming into a
figure. Papers get a second, parallel output instead — the real
`@excalidraw/excalidraw` React component, mounted live in the reader's own
browser in read-only `viewMode`, fed the actual scene JSON instead of a
picture of it.

Every other page on the site is completely unaffected: the SVG pipeline is
untouched, and the ~8MB viewer bundle only ever loads on a page that
actually has a papers mount point.

## Authoring: two supported models

### 1. Standalone `.excalidraw.md` (recommended)

Any file at `docs/papers/**/*.excalidraw.md` — at any nesting depth, group
however you like (`docs/papers/systems/raft.excalidraw.md`,
`docs/papers/ml/attention/paper.excalidraw.md`, ...) — becomes its own
page automatically. No frontmatter needed.

Write your notes directly at the top of the file, above Obsidian's own
`==⚠ Switch to EXCALIDRAW VIEW...==` line:

```markdown
---
excalidraw-plugin: parsed
tags: [excalidraw]
---
## My notes on this paper

Whatever you want here — this is real page content.

==⚠  Switch to EXCALIDRAW VIEW...==   <- everything from here down is
# Excalidraw Data                         Obsidian's own bookkeeping and
## Text Elements                          is stripped from the rendered
...                                        page. Never edit it by hand.
```

Only the part above that line survives into the built page; everything
from that line down (the auto-generated `# Excalidraw Data` / `## Text
Elements` / the compressed-json blob itself) is internal to Obsidian's
Excalidraw plugin and is stripped before rendering — but stays in the
source file untouched, so Obsidian's own live preview keeps working.

### 2. Folder + `index.md` + scene file

The older shape, still supported: `docs/papers/<slug>/index.md` with
`template: papers.html` frontmatter, plus a co-located scene file (embed it
with `![[scene.excalidraw]]` so it also gets a static SVG thumbnail, e.g.
for `docs/papers/index.md`'s own listing). If the scene file isn't named
`scene.excalidraw.md`, add `papers_scene: <basename>` to the page's
frontmatter.

Use this when you want your own title/description frontmatter separate
from the scene, or a page that isn't 1:1 with a single scene.

### Annotating a PDF

Import the PDF into Excalidraw (Obsidian's Excalidraw plugin: insert PDF
page as image) and draw over it as usual. This is a "soft embed" —
Obsidian stores it as a link (`## Embedded Files` section mapping a
`fileId` to `[[../pdfs/paper.pdf#page=N]]`), not baked-in pixel data, so
nothing outside Obsidian could render it before this pipeline resolved
that link itself (see "PDF/image resolution" below). Put raw PDFs in
`docs/papers/pdfs/` — that folder is never treated as scene content, and
`.pdf` files there are just copied through to the built site like any
other static asset (never excluded, so also directly linkable if wanted).

## Architecture

### 1. `scripts/render_excalidraw.py` — additive `scene.json` output

For every scene under `docs/papers/`, in addition to (never instead of)
the normal SVG job, the same decompressed `elements`/`appState`/`files`
already in hand gets dumped to `<scene-basename>.excalidraw.json` next to
the scene file — named after the scene itself (matching the SVG's own
`<base>.excalidraw.svg` convention), not a flat `scene.json`, so multiple
papers can safely be siblings under a shared field-grouping folder.
Cached in the manifest the same way as SVGs (`papersJson` field, mirroring
`svg`).

**Reference-driven only for the SVG** — a papers scene always gets its
`scene.json` (the folder convention under `docs/papers/` is itself the
trigger, no embed needed), but the SVG thumbnail stays strictly opt-in via
an actual `![[...]]` embed somewhere, exactly like every other scene on
the site.

### 2. PDF/image resolution (`resolve_embedded_files`)

Obsidian's `## Embedded Files` section is parsed directly from the scene's
markdown (outside the compressed-json blob, which never contains this
data). For each `fileId: [[path#page=N]]` entry not already present in
`files`:
- `.pdf` + `#page=N` → rasterized with PyMuPDF (`pymupdf`, imported as
  `fitz`) to a PNG, base64-encoded into a proper Excalidraw
  `BinaryFileData` entry.
- Plain image file → read and base64-encoded directly.

This runs for every scene site-wide (not just papers) — any existing note
using this same Obsidian embed pattern for plain images gets the same fix
for free. Resolution is lazy per scene (only pays the rasterization cost
on an actual cache miss, not on every run).

### 3. Viewer bundle (`scripts/excalidraw-render/`)

`build.mjs` gained a second esbuild entry point, `src/viewer-entry.js`
(sibling to the existing SVG-export `harness-entry.js`): mounts
`<Excalidraw viewMode={true} initialData={...} />` via
`ReactDOM.createRoot`, fetching the page's own `scene.json`-equivalent
file. Minified (~8MB), output + fonts copied to `docs/assets/papers/` so
`mkdocs build` picks it up through its normal `docs/` → `site/` copy.

### 4. `overrides/papers.html` — the per-page template

mkdocs-material's `template:` frontmatter, applied automatically (see
below) for standalone scenes, or by hand for the folder+index.md model.
Renders the mount div (`#papers-viewer`), widens the content column and
hides the right-hand TOC rail (`!important` — safe, this stylesheet only
ever loads on papers pages), and reads
`page.meta.papers_scene_json | url` for the correct scene-data URL — the
`| url` filter is what makes this resolve correctly regardless of page
depth, see the next section for why that's not just a bare relative path.

### 5. `scripts/excalidraw_embed_hook.py` — where the two models converge

`on_page_markdown` sets `page.meta['papers_scene_json']` (a docs-relative
path to the `.excalidraw.json` file) for both models, which
`overrides/papers.html` then just reads:
- **Standalone scene**: also sets `page.meta['template'] = 'papers.html'`
  and strips the markdown down to whatever's above Obsidian's `==⚠...==`
  line. The scene's own directory is *not* the same depth as the page's
  final URL once `use_directory_urls` turns `foo.excalidraw.md` into
  `foo.excalidraw/` — the `| url` filter (not a bare relative string)
  is what accounts for that extra nesting level correctly.
- **Folder+index.md**: reads `page.meta.papers_scene` frontmatter
  (default `"scene"`), computed relative to the page's own directory —
  here the page and the scene file are already co-located at the same
  depth, so this is the simpler case.

`docs/papers/**/*.excalidraw.md` is carved out of `mkdocs.yml`'s
`exclude_docs` (`!papers/**/*.excalidraw.md`) — everywhere else, raw scene
files stay excluded from the build as before.

### 6. Loading the viewer bundle without breaking `navigation.instant`

`docs/src/js/papers-loader.js` — small, site-wide (in `extra_javascript`,
so present on every page, but a no-op unless it finds `#papers-viewer`).
**Why this exists**: `navigation.instant` swaps `<body>` content via fetch
on in-site link clicks; a `<script>` tag declared only in a per-page
template never gets injected for a reader arriving from elsewhere on the
site, so a static tag in `overrides/papers.html` would silently fail to
load on exactly that navigation path (confirmed via headless testing — it
works on a hard page load, fails on SPA navigation, unless handled this
way). The loader dynamically injects the real bundle on both a hard load
and every `document$` swap, one code path for both.

## Folder structure

```
docs/papers/
  pdfs/<paper>.pdf              raw PDFs, shared, never scene content
  <field>/<paper>.excalidraw.md group however you like, any depth
  <slug>/index.md + scene.excalidraw.md   older co-located model
  index.md                      hand-written listing page
```

## Build wiring

`deploy.sh` and `serve.sh` both run `(cd scripts/excalidraw-render && npm
run build)` before the `mkdocs build`/`serve` call, alongside the existing
`render_excalidraw.py` step. See `EXCALIDRAW_RENDERING.md`'s "One-time
setup" for the rest of the toolchain (Node deps, Playwright); add `pip
install pymupdf` for PDF rasterization.

## Known gaps

- **Page titles** for the standalone-scene model come straight from the
  filename (e.g. `resume.excalidraw.md` → "Resume.excalidraw") — a bit
  ugly. Add a `title:` frontmatter override by hand if it bothers you;
  nothing automatic yet.
- **`scene.json` size**: a PDF-page-embedding scene can be several MB
  (base64 raster images per page) — noticeably heavier than a normal
  diagram's `scene.json`. Not a correctness problem, just don't expect it
  to be small.
- **Search doesn't index canvas content**: the live viewer mounts
  client-side, so mkdocs' search plugin only ever sees the page's own
  title/description/notes text, never anything drawn inside the scene.
