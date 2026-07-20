# Excalidraw scene rendering

How `.excalidraw.md` scenes become real SVG diagrams in the built site,
without breaking Obsidian, without external services, and without
committing manual PNG exports.

## The problem this solves

Excalidraw scene JSON isn't self-describing — it only becomes a diagram
once run through Excalidraw's own renderer (RoughJS for the sketchy
strokes, real browser font-metrics for text layout). There's no
lightweight/pure-Python way to render one; every credible approach reduces
to "a real browser running the real `@excalidraw/excalidraw` package."
Manually exporting a PNG from Obsidian and pasting it into `assets/` was
the workaround before this pipeline existed, and it doesn't scale or stay
in sync with the source scene.

## Authoring: the only thing you need to know day-to-day

In any `.md` file, embed a scene using Obsidian's native transclusion
syntax — the same thing Obsidian itself renders live in edit/preview mode:

```markdown
![[scene.excalidraw.md]]                    whole scene
![[scene.excalidraw.md#^frame=<frameId>]]    just one named Frame
![[scene.excalidraw.md#^frame=<frameId>|500]] ...with a pixel width
```

The `.md` extension is optional (`![[scene.excalidraw]]` works the same —
Obsidian lets you drop the extension on wikilinks to markdown files, and
this pipeline honors that too). The link target can be written in any of
the three ways Obsidian itself supports (depends on your vault's "New link
format" setting), all resolved the same way here as in Obsidian:

- **Relative to the note doing the embedding** — `../Excalidraw/scene`,
  `assets/scene`, etc. ("Relative path to file" setting.) Resolved against
  the referencing note's own folder, not vault root — so the same link
  text written in two different notes can correctly mean two different
  scenes.
- **Relative to vault root** — the full `docs/`-relative path. ("Absolute
  path in vault" setting.)
- **Shortest unique path** — just `scene`, if that name is unambiguous
  across the whole vault. (Obsidian's default setting.)

**A scene with no Frame just embeds as its whole canvas.** Frames are
opt-in, for when you want to surface one specific region of a bigger
working canvas instead of the whole thing — draw a Frame around it in
Excalidraw, give it a name, embed with `#^frame=`.

Nothing renders unless something actually embeds it. Scenes sitting in
`docs/` unreferenced by any `![[...]]` are never touched — see
"Reference-driven, not discovery-driven" below.

You keep editing this `![[...]]` form directly in Obsidian, forever. It is
**never rewritten**. What you see in `mkdocs serve`/the built site is a
resolved image — see "Where the substitution actually happens" below for
why the two can diverge without one ever touching the other.

## Architecture: three layers

```
┌────────────────────────────┐
│ 1. Node harness              scripts/excalidraw-render/
│    (real Excalidraw)         harness-entry.js, build.mjs, render.mjs
└──────────────┬─────────────┘
               │ invoked as a subprocess, once per batch
┌──────────────▼─────────────┐
│ 2. Python orchestrator       scripts/render_excalidraw.py
│    (what needs rendering,    reference-driven discovery, content-hash
│     caching, writes SVGs)    cache, manifest read/write
└──────────────┬─────────────┘
               │ writes docs/.excalidraw-manifest.json
┌──────────────▼─────────────┐
│ 3. MkDocs build hook         scripts/excalidraw_embed_hook.py
│    (embed → image, in        on_page_markdown: rewrites ![[...]] to
│     memory, at build time)   ![]() in the markdown mkdocs converts to
│                               HTML. Also on_pre_build: re-runs layer 2
│                               before every build/rebuild.
└─────────────────────────────┘
```

### 1. Node harness (`scripts/excalidraw-render/`)

- `package.json` — a small Node sub-project: `@excalidraw/excalidraw`
  (the real renderer, not a reimplementation), `playwright` (drives a real
  headless Chromium), `esbuild` (bundles the harness for fully offline use
  — no unpkg/CDN calls at render time, unlike some other Excalidraw-export
  tools).
- `src/harness-entry.js` — imports `exportToSvg`/`restore` from
  `@excalidraw/excalidraw`, sets `window.EXCALIDRAW_ASSET_PATH = "/"` so
  fonts resolve from a locally-served copy instead of unpkg, exposes
  `window.__excalidrawRenderToSvg(sceneData, frameId)`.
- `build.mjs` (`npm run build`) — bundles that entry with esbuild into
  `dist/harness.js`, copies the package's own font files into `dist/fonts`,
  copies `harness.html`. One-time, or whenever the harness source or
  Excalidraw version changes — not per render.
- `render.mjs` — the only piece that talks to Playwright/Chromium. Reads a
  JSON batch file (`{"jobs": [...]}`) from argv, serves `dist/` over a
  throwaway local HTTP server, launches **one** browser + one page, loops
  the batch calling the harness's render function, writes each result SVG
  to disk, prints a JSON result array to stdout. One browser launch per
  invocation, not per diagram — the fixed cost is the launch (~3s
  cold), not per-scene work.

### 2. Python orchestrator (`scripts/render_excalidraw.py`)

This is the only piece that understands the rest of the repo. Runs from
repo root (`python3 scripts/render_excalidraw.py`), no arguments needed for
normal use.

**Reference-driven, not discovery-driven.** This is the core design
decision: a scene file existing under `docs/` is never, by itself, a
reason to render or write anything. `SKIP_DIRS` (genuine non-content noise
only — mkdocs theme assets, Obsidian's own config, the reusable shape
library) is deliberately the *only* thing excluded from scene lookup;
gitignore status is never a factor, and neither is which folder a scene
happens to sit in — including `docs/Excalidraw/`, Obsidian's default save
location for a brand-new drawing. Being reference-driven already makes any
extra "is this really content" filtering redundant: a scene nobody embeds
is never touched, no matter where it lives. The script:

1. Scans every `.md` file under `docs/` for the `![[...excalidraw...]]`
   embed pattern, recording which file each embed came from
   (`discover_references`).
2. Resolves each (referencing file, link target) pair to an actual scene
   file on disk (`resolve_scene_path`), trying, in order: relative to the
   referencing file's own folder, relative to vault root, then a
   shortest-unique-path suffix match — matching all three of Obsidian's
   link format settings (see "Authoring" above).
3. Groups references by scene, so a scene embedded from several notes (or
   with several different Frames referenced) is only decompressed once.
4. For each referenced scene: strips the `` ```compressed-json `` fence,
   decompresses via `lzstring` (pure-Python port of Obsidian's own
   compression), parses the scene JSON, and computes only the blocks that
   were actually asked for — the whole-scene block, specific named-Frame
   blocks, or both.
5. Content-hashes each needed block (see caching below) against
   `docs/.excalidraw-manifest.json`; anything not already cached becomes
   one entry in a single batch handed to `render.mjs`.
6. Writes each newly-rendered SVG next to its source scene
   (`assets/<scene>.excalidraw.svg` for the whole scene,
   `assets/<scene>.excalidraw__<frame-name>.svg` per Frame), and updates
   the manifest.

**Never touches an authored `.md` file.** The only files this script ever
writes are generated SVGs and the manifest. It has no code path that opens
a non-generated `.md` for writing.

### 3. MkDocs build hook (`scripts/excalidraw_embed_hook.py`)

Wired in via `hooks:` in both `mkdocs.yml` and `mkdocs_local.yml`. Two
hook functions:

- **`on_page_markdown(markdown, page, ...)`** — called by mkdocs for every
  page, with that page's raw markdown, before it's converted to HTML.
  Regex-substitutes `![[scene.excalidraw...]]` → `![](relative/path.svg)`
  (with a `{: width="..." }` attr_list suffix if a width was given) **in
  that in-memory string only**. The `.md` file on disk is never opened for
  writing by this hook. It reads `docs/.excalidraw-manifest.json` (cached
  in-process after first read) to resolve embeds to SVG paths; if a scene
  hasn't been rendered (or a referenced Frame no longer exists), the embed
  is left as-is rather than breaking the build with a dead link.
- **`on_pre_build(config, ...)`** — called before every build, including
  every incremental rebuild `mkdocs serve`'s file-watcher triggers, not
  just the very first one. Shells out to `render_excalidraw.py` so the
  manifest/SVGs are current before `on_page_markdown` runs. This is what
  makes editing a scene mid-`mkdocs serve` actually show up without a full
  restart — see the mtime/rebuild-loop gotcha below for why this needed
  care.

### Where the substitution actually happens

Your `.md` source always has `![[scene.excalidraw.md#^frame=id]]` in it —
that never changes, so Obsidian's live preview/transclusion keeps working
exactly as it always did. The substitution to a real `<img>` only exists
in mkdocs's in-memory copy of that markdown, produced fresh on every
build. Repoint a note at a different frame, or from a frame to the whole
scene (or vice versa), and the next build just reflects it — nothing to
"fix" in the source, because nothing there was ever wrong.

## Caching

`docs/.excalidraw-manifest.json` maps `"<scene-path>::<block-name>"` to
`{hash, svg, frameId}`. A block is a cache hit iff the stored hash matches
a fresh hash of the block's current content **and** the target SVG file
still exists on disk; otherwise it's a miss and gets re-rendered.

The hash is `sha256` of the block's elements (each element with
`version`/`versionNonce`/`updated` stripped — see below) plus the scene's
`viewBackgroundColor`, JSON-serialized with sorted keys for determinism.

**Why those three fields are stripped:** Excalidraw bumps
`version`/`versionNonce`/`updated` on an element on every touch-and-save,
including just having the file open in Obsidian while something nearby
changes — with zero visual effect. Hashing them made the cache flap
(false-positive "changed") purely from the vault being open live in
Obsidian, independent of any real edit. Confirmed by testing: two
back-to-back `--verify-cache` runs with no edit in between produced a
mismatch before this fix, stable after.

## Orphan handling

An orphan is a manifest entry whose key no longer corresponds to anything
currently referenced (embed removed from a note, Frame renamed/deleted,
etc.).

**Orphans are reported, never deleted automatically.** A normal run prints
each orphaned key and its stale SVG path to stderr and stops there — the
file and manifest entry are left alone. Deletion only happens if you pass
`--prune-orphans` explicitly. A script run should never be able to make a
file disappear as a side effect of something unrelated changing.

## The `mkdocs serve` infinite-rebuild-loop gotcha

Worth understanding if you ever touch this pipeline again: `on_pre_build`
writes `docs/.excalidraw-manifest.json`, which lives inside `docs/` — the
exact directory `mkdocs serve`'s watcher watches. If that write happened
unconditionally on every run (even when nothing actually changed), it
would bump the file's mtime every time, which the watcher reads as "this
changed, rebuild" — which runs `on_pre_build` again — which writes the
file again — forever, even after the cache has genuinely settled.

Fixed in `save_manifest()`: it compares the serialized bytes it's about to
write against what's already on disk and returns without writing at all
if they're identical. A real edit still causes exactly one extra rebuild
cycle (expected — the new SVG needs to be picked up); the cycle after that
makes zero writes anywhere under `docs/`, so the watcher goes idle.

## CLI flags

```
python3 scripts/render_excalidraw.py [flags]

--dry-run        Print what would render/skip without writing anything.
--verify-cache   Read-only. Exits non-zero and prints exactly which
                 key(s) are stale (mismatched hash or missing file) or
                 orphaned. Useful as a quick regression check.
--prune-orphans  Actually delete orphaned SVGs + manifest entries.
                 Without this flag, orphans are only reported.
```

## One-time setup

See `setup.txt` for the exact commands. Summary:

```bash
pip install lzstring                     # in the repo's .venv

cd scripts/excalidraw-render
npm install                              # playwright, @excalidraw/excalidraw, esbuild
npx playwright install chromium          # ~95MB, one-time browser download
npm run build                            # bundles dist/harness.js + fonts
```

## Where things live / what's gitignored

- Generated SVGs: committed, next to their source scene
  (`docs/**/assets/*.excalidraw*.svg`) — same convention as manually
  pasted images.
- `docs/.excalidraw-manifest.json`: committed — it's the cache, and
  committing it means a fresh clone doesn't have to re-render everything.
- `scripts/excalidraw-render/node_modules/` and `dist/`: gitignored build
  artifacts, regenerated by `npm install && npm run build`.
- `docs/tmp/`: already gitignored (pre-existing repo convention, unrelated
  to this pipeline) — used as the scratch/proving-ground for this feature
  itself (`docs/tmp/scratch.md` + `scratch.excalidraw.md`).
- `docs/Excalidraw/`: Obsidian's default save location for a brand-new
  drawing. `.gitignore` excludes `*.excalidraw.md`/`*.excalidraw` there
  specifically, but **not** `*.svg` — so if you embed a scene straight out
  of that folder, the rendered SVG gets committed while its source stays
  gitignored (unless that particular scene happens to already be tracked
  from before). That's a real asymmetry, not a bug: it means a diagram
  rendered from that folder isn't reproducible/verifiable from a fresh
  clone the way every other scene in this pipeline is, since the source
  behind it isn't in git. Deliberately not fixed automatically — moving
  the scene into a real `docs/<topic>/assets/` folder (like every other
  scene) removes the asymmetry entirely; whether that matters for a given
  scene is a per-case call, not something this pipeline should decide for
  you.

## Known gaps (not fixed by this work, flagged for later)

- Two scene files use `excalidraw-plugin: parsed` frontmatter instead of
  the `.excalidraw.md` suffix (`docs/sd/lld/problems/assets/tic_tac_toe.md`,
  `docs/dsa/ll/assets/lld.excalidraw.png.md`). `mkdocs.yml`'s
  `exclude_docs` doesn't cover them, and `mkdocs_local.yml` has no
  `exclude_docs` at all — they may render as broken standalone pages,
  independent of anything in this pipeline.
- Existing manually-exported PNGs (`![](assets/x.png)`) are not
  auto-migrated to the `![[...]]` form. That's an intentional,
  per-note, whenever-you-get-to-it decision, not an oversight — see the
  changelog for why.
