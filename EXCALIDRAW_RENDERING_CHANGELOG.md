# Excalidraw rendering — session log, 2026-07-20

Full chronological record of building the pipeline documented in
`EXCALIDRAW_RENDERING.md`, including the mistakes made along the way and
how they were caught — kept because the corrections are as informative as
the final design. Not committed by Claude; left for manual review first.

## 1. Initial implementation

Built the three-layer pipeline from scratch, following a pre-written plan
(`projects/notes/raw/excalidraw-mkdocs-rendering.md` in the personal vault):

- `scripts/excalidraw-render/` — Node sub-project (Playwright +
  `@excalidraw/excalidraw` + esbuild-bundled offline harness).
- `scripts/render_excalidraw.py` — Python orchestrator: discovery,
  lz-string decompression, content-hash caching, single-batch subprocess
  call to the Node renderer.
- Wired into `deploy.sh`/`serve.sh`, deps appended to `setup.txt`,
  `node_modules`/`dist` gitignored.

First block model: a scene with no Frame rendered as one implicit
"default" whole-scene block (matching the plan's original spec, since no
Frames existed anywhere in the vault at the time).

**Validated, not just assumed:** cold run rendered all 64 then-existing
scenes clean — zero `NaN` text positions (the exact failure mode that
ruled out other tools during research), real font-shaped SVGs. No-op
rerun confirmed byte-identical manifest/SVGs via `diff`, not just
eyeballing. Single-scene-edit rerun re-rendered exactly the affected
scene. Full `mkdocs build` succeeded, picked up the one intentionally
fixed reference (`high_throughput_3.md`'s dangling PNG link → the new
SVG) with correct `glightbox` lightbox wrapping.

## 2. First user correction — Frame-only publishing model

User: bring back the ability to render only Frame-marked content; a scene
with no Frame should produce **nothing**, not a default whole-scene
render.

Applied. This orphaned all 64 just-rendered SVGs (none had Frames) — the
existing orphan-cleanup mechanism deleted them automatically once the
model changed. Consequence: `high_throughput_3.md`'s fix from step 1 had
to be reverted (that scene has no Frame), confirmed with the user rather
than silently leaving a claim of "fixed" that wasn't true anymore.

**Real bug found here:** the content-hash cache was unstable on a vault
actively open in Obsidian — Excalidraw bumps `version`/`versionNonce`/
`updated` on elements just from the file being open, no visual change
involved. `--verify-cache` flagged a false mismatch one run after a clean
render. Fixed by excluding those three fields from the hash payload.

## 3. Second user correction — non-destructive embed resolution

User: the frame-embed resolution (`![[scene#^frame=id]]` → SVG) must not
rewrite the referencing `.md` **on disk** — that permanently destroys the
live Excalidraw-frame preview in Obsidian every time the build runs, and
the user repoints frames often.

This was a real architecture mistake, not a refinement: the original
implementation opened the referencing note and replaced the wikilink with
a plain `![]()` tag, in place. Fixed by splitting the concern properly:

- `render_excalidraw.py` never touches an authored `.md` file, full stop.
- New `scripts/excalidraw_embed_hook.py`, an mkdocs `on_page_markdown`
  hook — resolves the same pattern but only in the in-memory markdown
  string mkdocs converts to HTML for that build. Verified by comparing
  the built HTML's `<img>` tags against the untouched `.md` source,
  byte-for-byte.

## 4. Third user correction — "if this works, we solved it?" reality check

User asked directly whether the original problem was solved. Answer given
plainly: the rendering mechanism was proven correct, but **zero of the 64
real diagrams actually rendered** — none had a Frame yet, and the specific
triggering bug (`high_throughput_3.md`'s dangling image) was still
broken. Distinguishing "the infrastructure works" from "the user's actual
notes are fixed" mattered here — they are not the same claim.

## 5. Fourth correction — bringing back whole-scene rendering, wrong assumption

User: "if a frame is not referenced, load the entire file" — read (at the
time) as: restore automatic whole-scene rendering for every scene, in
addition to Frame blocks. Implemented: `detect_blocks` always produces a
`default` block; `![[scene.excalidraw.md]]` (no anchor) resolves to it.

**Assumption made without verifying it:** that "whole scene" render was
equivalent to what the user's existing manual PNG exports represented.
This was wrong, and got corrected in step 6.

## 6. Fifth correction — reference-driven, not discovery-driven (the big one)

User pushed back hard, correctly, on two points:

1. The manual PNGs were selective crops, not full-canvas exports — the
   "restore whole-scene rendering" change in step 5 didn't actually match
   the user's real workflow, it was an assumption dressed up as a fact.
2. Much more important: the pipeline had become **discovery-driven** —
   render anything found under `docs/`, whether or not anything asked for
   it. That produced 65 unwanted SVGs scattered across real directories,
   including all of `docs/sd/hld/`, none of which were requested.

Rewrote the core loop to be reference-driven: scan every `.md` for the
embed pattern *first*, resolve each reference to an actual scene/block,
and only decompress/render exactly those. A scene existing on disk is
never, by itself, a reason to touch anything. The existing orphan
mechanism did the actual cleanup of the 65 files for free once the
architecture changed — no separate deletion step was needed. Side
benefit: run time dropped from ~18-28s to ~0.5s (no longer decompressing
every scene on every run, just the referenced ones).

Verified: exactly the 2 SVGs actually referenced (in `docs/tmp/scratch.md`)
remained anywhere in the repo; `git status --porcelain -- docs/sd/hld`
empty; full `mkdocs build` still succeeded.

## 7. Sixth correction — orphans must never auto-delete

Even though the reference-driven fix's auto-deletion of the 65 files was
*correct* that time, the user objected to the principle: a script run
should never be able to delete files as a side effect, regardless of
whether the deletion happens to be right. Changed orphan handling to
report-only by default; deletion now requires explicit `--prune-orphans`.
Verified by injecting a fake orphaned manifest entry + stale file: a plain
run reports it and leaves it alone, `--prune-orphans` still removes it
correctly when asked.

## 8. Two real bugs found by direct user testing

User tried `![alt](url)` markdown-image syntax pointing at a scene file —
doesn't work, and shouldn't: that's not Obsidian's transclusion syntax
(`![[...]]` is), it's standard markdown expecting an actual image asset.
Explained rather than "fixed" — there was nothing broken.

User correctly flagged that Obsidian allows dropping `.md` from wikilinks
to markdown files (`![[scene.excalidraw]]`, no extension) — this pipeline
didn't support that form yet. Fixed in both `EMBED_RE` patterns (kept in
sync by hand between `render_excalidraw.py` and
`excalidraw_embed_hook.py`) and the scene-path resolver.

User also reported `mkdocs serve` only picking up scene edits on a full
restart, never live. Root cause: mkdocs hooks are loaded once at server
start; nothing was re-running the render step on each incremental
rebuild. Added `on_pre_build` to the hook to fix it — verified the
underlying staleness bug against the user's own already-running server
(one small, immediately-reverted test edit, confirmed via
`--verify-cache` that the revert was byte-perfect), but did **not** get
a live confirmation of the fix itself, since starting a second test
server instance failed (port already bound by the user's session). Asked
the user to verify directly rather than claiming success without
evidence.

## 9. Seventh correction — self-inflicted infinite rebuild loop

The `on_pre_build` hook from step 8 wrote `docs/.excalidraw-manifest.json`
unconditionally on every run, even when content was unchanged. That file
lives inside `docs/`, which `mkdocs serve` watches — an unconditional
rewrite bumps its mtime every time, which the watcher reads as "changed",
triggering another rebuild, which runs the hook again, forever. Fixed by
comparing serialized bytes against what's on disk before writing, skipping
the write entirely when unchanged. Verified via direct mtime comparison
across a no-op rerun (unchanged before the fix would have kept bumping;
confirmed stable after).

## 10. Documentation pass (this file + EXCALIDRAW_RENDERING.md)

While writing `EXCALIDRAW_RENDERING.md`, re-reading `render_excalidraw.py`
end-to-end surfaced one more latent bug from step 8's `.md`-optional fix:
`discover_references`'s fast pre-filter still checked for the literal
substring `.excalidraw.md`, so a note using *only* the extension-less
form (and no other `.excalidraw.md`-suffixed reference elsewhere in the
same file) would be silently skipped entirely. Fixed (`.excalidraw.md` →
`.excalidraw` in the pre-filter), verified against a synthetic
extension-less-only test string, re-ran `--verify-cache` clean afterward.

## 11. Two more real bugs, found testing a relative-path embed

User tried `![[../Excalidraw/scratch.excalidraw#^frame=id]]` (a relative
link, going up from `docs/tmp/` into `docs/Excalidraw/`) and asked why it
wasn't rendering. Two separate real issues, not one:

- **Path-resolution bug:** `resolve_scene_path` only ever resolved a link
  target relative to `docs/` itself, never relative to the referencing
  note's own folder — so a `../`-style relative link (Obsidian's
  "relative path to file" link format) resolved to the wrong location
  entirely, silently. Fixed by trying, in order: relative to the
  referencing file's folder, relative to vault root, then a
  shortest-unique-path suffix match — covering all three of Obsidian's
  link format settings. Required threading the referencing file's path
  through `discover_references` (previously just a flat set of link
  strings with no notion of which file they came from — insufficient once
  the same link text can mean different things depending on where it's
  written). Applied identically to `excalidraw_embed_hook.py`'s
  resolution, which had the same bug. Verified the resolution math
  directly against a synthetic known-scenes list before it was fully
  wired up, then end-to-end once wired.

- **Flawed premise, caught by direct user pushback:** `docs/Excalidraw/`
  (Obsidian's default save location for a new drawing) was excluded from
  scene discovery entirely, reasoning that it was gitignored so shouldn't
  be treated as real content. The user pushed back directly: gitignore
  controls what gets *committed*, not what a local dev tool should
  *discover* — those are unrelated concerns, and conflating them was the
  actual mistake. The reference-driven architecture already provides the
  real safety guarantee (nothing renders unless something explicitly
  embeds it); the directory-level skip was inherited wholesale from
  `generate_llms_txt.py`, where it solves a different problem (avoid
  listing scratch files as wiki pages), and never actually did anything
  useful here. Removed the "Excalidraw"-prefix skip entirely. Flagged
  (not fixed, and not this pipeline's decision to make) the one genuine
  remaining consequence: `.gitignore` still excludes
  `docs/Excalidraw/*.excalidraw.md` specifically, so a brand-new,
  never-committed scene embedded straight from that folder would have its
  rendered SVG committed with no source behind it in git. Documented in
  `EXCALIDRAW_RENDERING.md`'s "Where things live" section rather than
  silently deciding either way.

Verified end-to-end: the exact scene from the user's test embed
(`docs/Excalidraw/scratch.excalidraw.md`) now resolves and renders
correctly (3 blocks, zero `NaN`), `docs/sd/hld/` still untouched.

## Net state at end of session

- `docs/sd/hld/` and every other pre-existing real-content directory:
  untouched, confirmed via `git status --porcelain` throughout.
- 6 SVGs exist in the repo: 3 under `docs/Excalidraw/` (currently
  referenced by `docs/tmp/scratch.md`, not gitignored — see the
  known-gap note above) and 3 stale-but-not-deleted under gitignored
  `docs/tmp/` (orphaned once `scratch.md` was repointed at
  `docs/Excalidraw/` instead; left in place per the report-only orphan
  policy — `--prune-orphans` would clean them up on request). Nothing
  renders for real content yet because no real note uses the `![[...]]`
  embed syntax yet — that migration is the user's own, at their own pace.
- Nothing committed. New/modified files, for review:
  - New: `scripts/excalidraw-render/` (Node sub-project),
    `scripts/render_excalidraw.py`, `scripts/excalidraw_embed_hook.py`,
    `docs/.excalidraw-manifest.json`, `EXCALIDRAW_RENDERING.md`,
    `EXCALIDRAW_RENDERING_CHANGELOG.md`.
  - Modified: `deploy.sh`, `serve.sh`, `setup.txt`, `.gitignore`,
    `mkdocs.yml`, `mkdocs_local.yml`, `README.md`,
    `docs/Excalidraw/scratch.excalidraw.md` (pre-existing tracked file,
    now has real Frame content again).
