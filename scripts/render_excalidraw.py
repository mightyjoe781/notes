#!/usr/bin/env python3
"""Render Excalidraw scenes under docs/ to real vector SVGs before `mkdocs build`.

Excalidraw scene JSON isn't self-describing -- it only becomes a diagram
once run through Excalidraw's own renderer (RoughJS sketchy strokes + real
browser font-metrics text layout). This script is the Python orchestrator:
it decompresses `` ```compressed-json `` scene data and shells out once to
scripts/excalidraw-render/render.mjs (a Node/Playwright script) with the
whole miss-batch, so a real headless Chromium + the real
@excalidraw/excalidraw package is launched at most once per build, not once
per diagram.

This is reference-driven, not discovery-driven: a scene existing under
docs/ is not, by itself, a reason to render anything. Something only gets
rendered if at least one .md file actually embeds it via Obsidian's native
syntax:
    ![[scene.excalidraw.md]]                 -> whole scene
    ![[scene.excalidraw.md#^frame=<id>]]      -> just that named Frame
Every referencing .md is scanned first; only the scenes/frames actually
named by some embed are decompressed and rendered. Nothing is rendered
"just in case". Anything that stops being referenced (embed removed, frame
renamed/deleted) is detected as an orphan and reported -- but never deleted
automatically. A run of this script should never make a file disappear as
a side effect of something unrelated changing. Pass --prune-orphans if you
actually want the stale SVGs + manifest entries cleaned up.

One deliberate exception: a scene at docs/papers/<slug>/scene.excalidraw.md
is always treated as referenced (whole-scene block only), with no embed
needed in its sibling index.md -- the folder convention itself is the
reference. See the docs/papers/ live viewer, PAPERS_PREFIX.

This script only ever writes generated SVGs (under docs/**/assets/, next to
the scene that produced them) and the manifest. It never touches an
authored .md file. Turning an embed into a real image reference is a
separate, non-destructive step done at mkdocs-build time by
scripts/excalidraw_embed_hook.py (an mkdocs `hooks:` entry, see mkdocs.yml /
mkdocs_local.yml) -- it rewrites the markdown in memory as mkdocs converts
it to HTML, so the .md source you edit in Obsidian never changes and keeps
its live Excalidraw preview. That hook reads the manifest this script
writes, so this script must run first.

Run from repo root (venv active): `python3 scripts/render_excalidraw.py`.
Wired into deploy.sh and serve.sh, ahead of `mkdocs build`/`mkdocs serve`,
same pattern as scripts/generate_llms_txt.py.

Flags:
  --dry-run        Print what would render/skip without writing anything.
  --verify-cache   Assert the on-disk cache is fully up to date; writes
                    nothing; exits non-zero and prints mismatches if stale.
  --prune-orphans  Actually delete orphaned SVGs + manifest entries (see
                    above). Without this flag orphans are only reported.
"""

import base64
import hashlib
import json
import mimetypes
import os
import re
import subprocess
import sys
import tempfile
import time

import pymupdf as fitz  # for rasterizing PDF-page embeds -- see resolve_embedded_files
import yaml
from lzstring import LZString

DOCS_DIR = "docs"
MANIFEST_PATH = os.path.join(DOCS_DIR, ".excalidraw-manifest.json")
RENDER_SCRIPT = os.path.join("scripts", "excalidraw-render", "render.mjs")

# Whole-scene blocks for any scene living under docs/papers/ additionally get
# their raw decompressed JSON (elements/appState/files) dumped next to the
# scene, for the live interactive Excalidraw viewer used there (see
# overrides/papers.html) -- everywhere else only ever gets a rendered SVG.
# This is purely additive: it never changes what happens on the SVG path.
PAPERS_PREFIX = os.path.join(DOCS_DIR, "papers") + os.sep

# Only used to resolve an embed's link target to an actual scene file (a
# link may be a full docs-relative path or a shorter Obsidian
# shortest-unique-path -- see resolve_scene_path). Not a render worklist: a
# scene appearing here is not by itself a reason to render anything -- that
# guarantee comes from being reference-driven, not from this list. So this
# only needs to exclude genuine non-content noise (mkdocs theme assets,
# Obsidian's own config, the reusable shape library), never a "should this
# be treated as real content" judgment call -- gitignore status is
# unrelated and deliberately not a factor here. docs/Excalidraw/ (Obsidian's
# default save location for a brand-new drawing) is intentionally NOT
# skipped: a scene sitting there is discoverable and renders fine the
# moment something actually embeds it, same as any other scene.
SKIP_DIRS = {"src", ".obsidian", "excalidraw_library"}

FENCE_RE = re.compile(r"```compressed-json\n(.*?)\n```", re.DOTALL)
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)

# Obsidian's Excalidraw embed syntax. The #^frame=<id> anchor is optional --
# a bare ![[scene.excalidraw]] or ![[scene.excalidraw.md]] means "the whole
# scene". The trailing ".md" is optional too -- Obsidian lets you drop the
# extension on wikilinks to markdown files, so link_target (group 1) never
# includes it; resolve_scene_path always appends ".md" when resolving
# against real files on disk. Kept in sync by hand with the identical
# pattern in scripts/excalidraw_embed_hook.py (that file resolves the same
# syntax at mkdocs-build time; this one decides what needs rendering in the
# first place).
EMBED_RE = re.compile(r"!\[\[([^\]|#]+\.excalidraw)(?:\.md)?(?:#\^frame=([^\]|]+))?(?:\|(\d+))?\]\]")

# Obsidian's own "## Embedded Files" section, e.g.:
#   7bfd403bede33415fb81efd6a90dd27c42c5f989: [[../pdfs/paper.pdf#page=1]]
# One of these exists per `image` element whose fileId isn't self-contained
# in the compressed-json (see resolve_embedded_files for why that matters).
EMBEDDED_FILE_RE = re.compile(r"^([0-9a-fA-F]+): \[\[([^\]]+)\]\]", re.MULTILINE)

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}

LZ = LZString()


def should_skip_dir(name: str) -> bool:
    return name in SKIP_DIRS


def read_frontmatter(text: str) -> dict:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def is_scene_file(path: str, text: str) -> bool:
    """A file is a scene if it's `<name>.excalidraw.md`, OR a plain `.md`
    carrying `excalidraw-plugin: parsed` frontmatter (two committed scenes
    use this second shape instead of the suffix)."""
    if path.endswith(".excalidraw.md"):
        return True
    if path.endswith(".md"):
        return read_frontmatter(text).get("excalidraw-plugin") == "parsed"
    return False


def walk_docs(docs_dir: str):
    for root, dirs, files in os.walk(docs_dir):
        dirs[:] = sorted(d for d in dirs if not should_skip_dir(d))
        for fname in sorted(files):
            if fname.endswith(".md"):
                yield os.path.join(root, fname)


def discover_scenes(docs_dir: str) -> list[str]:
    """Every scene file that exists on disk -- a lookup index for resolving
    embed link targets, not a list of things to render."""
    scenes = []
    for fpath in walk_docs(docs_dir):
        try:
            text = open(fpath, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        if is_scene_file(fpath, text):
            scenes.append(fpath)
    return scenes


def discover_references(docs_dir: str) -> list[tuple[str, str, str | None]]:
    """Scan every .md file for Obsidian's Excalidraw embed syntax. Returns
    (referencing_file, link_target, frame_id_or_None) -- the referencing
    file matters because a relative link target (e.g. "../Excalidraw/x",
    Obsidian's "relative path to file" link format) resolves differently
    depending on which note it's written in, so the same link_target string
    from two different notes can mean two different scenes."""
    refs: list[tuple[str, str, str | None]] = []
    seen: set[tuple[str, str, str | None]] = set()
    for fpath in walk_docs(docs_dir):
        try:
            text = open(fpath, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        if "![[" not in text or ".excalidraw" not in text:
            continue
        for match in EMBED_RE.finditer(text):
            ref = (fpath, match.group(1), match.group(2))
            if ref not in seen:
                seen.add(ref)
                refs.append(ref)
    return sorted(refs, key=lambda r: (r[0], r[1], r[2] or ""))


def resolve_scene_path(
    referencing_file: str, link_target: str, docs_dir: str, known_scenes: list[str]
) -> str | None:
    """link_target never includes the optional ".md" (EMBED_RE strips it);
    real scene files on disk always end in ".excalidraw.md". Tries, in
    order: relative to the referencing file's own directory (handles both
    same-folder links and "../"-style relative links -- Obsidian's
    "relative path to file" link format), then vault-root-relative
    (Obsidian's "absolute path in vault" format), then a unique
    shortest-unique-path suffix match (Obsidian's default link format)."""
    suffix = link_target + ".md"

    relative_to_referencer = os.path.normpath(os.path.join(os.path.dirname(referencing_file), suffix))
    if relative_to_referencer in known_scenes:
        return relative_to_referencer

    relative_to_docs_root = os.path.normpath(os.path.join(docs_dir, suffix))
    if relative_to_docs_root in known_scenes:
        return relative_to_docs_root

    candidates = [s for s in known_scenes if s.endswith(suffix)]
    return candidates[0] if len(candidates) == 1 else None


def decompress_scene(path: str) -> dict | None:
    text = open(path, encoding="utf-8", errors="ignore").read()
    match = FENCE_RE.search(text)
    if not match:
        print(f"warning: {path}: no compressed-json fence, skipping", file=sys.stderr)
        return None
    compact = "".join(match.group(1).split("\n"))
    try:
        decompressed = LZ.decompressFromBase64(compact)
        if decompressed is None:
            raise ValueError("decompressFromBase64 returned None")
        data = json.loads(decompressed)
    except Exception as exc:  # noqa: BLE001 - report and skip, don't crash the whole build
        print(f"warning: {path}: failed to decompress scene json ({exc}), skipping", file=sys.stderr)
        return None
    return data


def rasterize_pdf_page(pdf_path: str, page_num: int, dpi: int = 150) -> bytes:
    doc = fitz.open(pdf_path)
    try:
        pix = doc[page_num - 1].get_pixmap(dpi=dpi)
        return pix.tobytes("png")
    finally:
        doc.close()


def resolve_embedded_files(scene_path: str, scene_text: str, files: dict) -> dict:
    """Fill in `files[file_id]` for images/PDF pages referenced only via
    Obsidian's "## Embedded Files" section (e.g. from importing a PDF page
    as an annotation background). Obsidian resolves that link live, using
    its own pdf.js integration, when the scene is open there -- but never
    writes the actual pixel data back into the compressed-json blob. Without
    this, every such image is invisible to anything outside Obsidian: it
    silently renders as nothing in both the static SVG export and the live
    browser viewer (docs/papers/), since standard Excalidraw only knows how
    to resolve `files[fileId]`, never a "[[relative/path#page=N]]" link.
    """
    embeds = dict(EMBEDDED_FILE_RE.findall(scene_text))
    if not embeds:
        return files

    resolved = dict(files)
    scene_dir = os.path.dirname(scene_path)
    for file_id, link in embeds.items():
        if file_id in resolved:
            continue  # already has real data -- nothing to resolve

        target, _, page_str = link.partition("#page=")
        page_num = int(page_str) if page_str.isdigit() else None
        embed_path = os.path.normpath(os.path.join(scene_dir, target))

        if not os.path.exists(embed_path):
            print(f"warning: {scene_path}: embedded file not found: {embed_path}", file=sys.stderr)
            continue

        try:
            if embed_path.lower().endswith(".pdf") and page_num is not None:
                raw = rasterize_pdf_page(embed_path, page_num)
                mime = "image/png"
            elif os.path.splitext(embed_path)[1].lower() in IMAGE_EXTS:
                with open(embed_path, "rb") as f:
                    raw = f.read()
                mime = mimetypes.guess_type(embed_path)[0] or "image/png"
            else:
                continue
        except Exception as exc:  # noqa: BLE001 - report and skip, don't crash the whole build
            print(f"warning: {scene_path}: failed to resolve embedded file {link} ({exc}), skipping", file=sys.stderr)
            continue

        resolved[file_id] = {
            "mimeType": mime,
            "id": file_id,
            "dataURL": f"data:{mime};base64,{base64.b64encode(raw).decode('ascii')}",
            "created": int(os.path.getmtime(embed_path) * 1000),
        }
    return resolved


def scene_basename(path: str) -> str:
    fname = os.path.basename(path)
    if fname.endswith(".excalidraw.md"):
        return fname[: -len(".excalidraw.md")]
    return fname[: -len(".md")]


def detect_blocks(elements: list[dict]) -> dict[str | None, dict]:
    """{frame_id_or_None: block}. frame_id None is the whole-scene block
    (only built lazily by the caller, when actually referenced); one entry
    per named Excalidraw Frame otherwise."""
    live_elements = [e for e in elements if not e.get("isDeleted")]
    blocks: dict[str | None, dict] = {
        None: {"frame_id": None, "name": "default", "elements": live_elements}
    }
    for frame in [e for e in live_elements if e.get("type") == "frame"]:
        name = frame.get("name") or frame["id"]
        members = [e for e in live_elements if e.get("frameId") == frame["id"]]
        blocks[frame["id"]] = {"frame_id": frame["id"], "name": name, "elements": [frame, *members]}
    return blocks


# Excalidraw bumps these on every touch-and-save of an element (including
# just having the file open in Obsidian while something nearby changes),
# with zero visual effect. Hashing them makes the cache flap on a vault
# that's actively open in Obsidian, not just on real content edits.
_VOLATILE_ELEMENT_KEYS = {"version", "versionNonce", "updated"}


def _stable_element(element: dict) -> dict:
    return {k: v for k, v in element.items() if k not in _VOLATILE_ELEMENT_KEYS}


def block_hash(elements: list[dict], app_state: dict) -> str:
    payload = {
        "elements": [_stable_element(e) for e in elements],
        "viewBackgroundColor": app_state.get("viewBackgroundColor"),
    }
    normalized = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def target_path(scene_path: str, block_name: str, frame_id: str | None) -> str:
    scene_dir = os.path.dirname(scene_path)
    base = scene_basename(scene_path)
    if frame_id is None:
        return os.path.join(scene_dir, f"{base}.excalidraw.svg")
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", block_name)
    return os.path.join(scene_dir, f"{base}.excalidraw__{safe_name}.svg")


def papers_json_path(scene_path: str) -> str:
    # Named after the scene itself (like target_path does for the SVG),
    # not a flat "scene.json" -- multiple papers can end up siblings under
    # the same field-grouping folder (docs/papers/<field>/...), and a
    # folder-only name would silently let one overwrite another's output.
    return os.path.join(os.path.dirname(scene_path), f"{scene_basename(scene_path)}.excalidraw.json")


def load_manifest() -> dict:
    if not os.path.exists(MANIFEST_PATH):
        return {}
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_manifest(manifest: dict) -> None:
    ordered = dict(sorted(manifest.items()))
    serialized = json.dumps(ordered, indent=2, sort_keys=True) + "\n"

    # Skip the write entirely if content is unchanged. This file lives
    # under docs/, which `mkdocs serve`'s watcher watches -- rewriting it
    # unconditionally bumps its mtime on every run (even true no-ops),
    # which the watcher reads as "changed", triggering another rebuild,
    # which runs this script again, which touches the file again... an
    # infinite rebuild loop that never settles. Only write when the bytes
    # actually differ.
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, encoding="utf-8") as f:
            if f.read() == serialized:
                return

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        f.write(serialized)


def run_render_batch(jobs: list[dict]) -> list[dict]:
    if not jobs:
        return []
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        json.dump({"jobs": jobs}, tmp)
        tmp_path = tmp.name
    try:
        proc = subprocess.run(
            ["node", RENDER_SCRIPT, tmp_path],
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            print(proc.stderr, file=sys.stderr)
            raise RuntimeError(f"{RENDER_SCRIPT} exited {proc.returncode}")
        return json.loads(proc.stdout)
    finally:
        os.unlink(tmp_path)


def main() -> None:
    dry_run = "--dry-run" in sys.argv
    verify_cache = "--verify-cache" in sys.argv
    prune_orphans = "--prune-orphans" in sys.argv

    if not os.path.isdir(DOCS_DIR):
        print("docs/ not found, run from repo root", file=sys.stderr)
        sys.exit(1)

    start = time.time()
    manifest = load_manifest()
    known_scenes = discover_scenes(DOCS_DIR)
    references = discover_references(DOCS_DIR)

    # Group resolved references by scene, so each referenced scene is only
    # decompressed once even if it's embedded from several notes / several
    # frames. This is what drives the SVG output specifically -- an
    # unreferenced scene never gets an SVG, papers scenes included (see
    # papers_scenes below for the separate, always-on trigger for their
    # scene.json).
    needed_frames_by_scene: dict[str, set[str | None]] = {}
    unresolved: list[str] = []
    for referencing_file, link_target, frame_id in references:
        scene_path = resolve_scene_path(referencing_file, link_target, DOCS_DIR, known_scenes)
        if scene_path is None:
            unresolved.append(f"{referencing_file}: {link_target}")
            continue
        needed_frames_by_scene.setdefault(scene_path, set()).add(frame_id)

    # Papers scenes are the one deliberate exception to "reference-driven,
    # not discovery-driven" -- but only for their scene.json, never the SVG.
    # A scene at docs/papers/<slug>/scene.excalidraw.md IS its own reason to
    # produce scene.json: the folder convention already unambiguously pairs
    # it with docs/papers/<slug>/index.md (the live viewer page that fetches
    # it), and requiring an embed in that same index.md just to keep the
    # pipeline running is redundant and easy to accidentally strip (e.g.
    # thinking it's an unused static thumbnail once the live viewer works).
    # The SVG stays strictly reference-driven like every other scene: it's
    # only ever a deliberate thumbnail, built when something actually embeds
    # this scene (e.g. docs/papers/index.md), never automatically.
    papers_scenes = {s for s in known_scenes if s.startswith(PAPERS_PREFIX)}

    current_keys: set[str] = set()
    hit_keys: set[str] = set()
    miss_jobs: list[dict] = []
    papers_miss_jobs: list[dict] = []
    mismatches: list[str] = []
    n_blocks = 0
    missing_frames: list[str] = []

    for scene_path in sorted(set(needed_frames_by_scene) | papers_scenes):
        data = decompress_scene(scene_path)
        if data is None:
            continue
        elements = data.get("elements", [])
        app_state = data.get("appState", {}) or {}
        files = data.get("files") or {}
        blocks_by_frame_id = detect_blocks(elements)

        # Resolving embedded PDF pages/images means rasterizing a PDF page
        # per file, which is real work -- only pay for it once, and only if
        # this scene actually has a cache miss to build (not on every run
        # once everything's cached). Memoized per scene, not per block: all
        # blocks of a scene share the same resolved files.
        _resolved_files: list[dict] = []

        def resolved_files() -> dict:
            if not _resolved_files:
                scene_text = open(scene_path, encoding="utf-8", errors="ignore").read()
                _resolved_files.append(resolve_embedded_files(scene_path, scene_text, files))
            return _resolved_files[0]

        is_papers_scene = scene_path in papers_scenes
        explicit_frame_ids = needed_frames_by_scene.get(scene_path, set())
        frame_ids_to_process = set(explicit_frame_ids)
        if is_papers_scene:
            frame_ids_to_process.add(None)  # scene.json always needs the whole-scene block, embed or not

        for frame_id in sorted(frame_ids_to_process, key=lambda f: f or ""):
            block = blocks_by_frame_id.get(frame_id)
            if block is None:
                if frame_id in explicit_frame_ids:
                    missing_frames.append(f"{scene_path}#^frame={frame_id}")
                continue

            block_name, block_elements = block["name"], block["elements"]
            key = f"{scene_path}::{block_name}"
            digest = block_hash(block_elements, app_state)

            want_papers = is_papers_scene and frame_id is None
            want_svg = frame_id in explicit_frame_ids

            # Independent of the SVG cache below -- runs even when the SVG
            # is a cache hit (or not wanted at all), so must never
            # `continue` past the SVG handling below.
            if want_papers:
                papers_key = f"{key}::papers-json"
                current_keys.add(papers_key)
                papers_path = papers_json_path(scene_path)
                papers_entry = manifest.get(papers_key)
                papers_cached_hash = papers_entry.get("hash") if isinstance(papers_entry, dict) else None
                papers_cache_hit = papers_cached_hash == digest and os.path.exists(papers_path)
                if papers_cache_hit:
                    hit_keys.add(papers_key)
                elif verify_cache:
                    mismatches.append(papers_key)
                else:
                    papers_miss_jobs.append(
                        {
                            "key": papers_key,
                            "path": papers_path,
                            "elements": block_elements,
                            "appState": app_state,
                            "files": resolved_files(),
                            "digest": digest,
                        }
                    )

            if not want_svg:
                continue

            n_blocks += 1
            current_keys.add(key)
            out_path = target_path(scene_path, block_name, frame_id)

            entry = manifest.get(key)
            cached_hash = entry.get("hash") if isinstance(entry, dict) else None
            cache_hit = cached_hash == digest and os.path.exists(out_path)

            if cache_hit:
                hit_keys.add(key)
                continue

            if verify_cache:
                mismatches.append(key)
                continue

            miss_jobs.append(
                {
                    "key": key,
                    "outputPath": os.path.abspath(out_path),
                    "elements": block_elements,
                    "appState": app_state,
                    "files": resolved_files(),
                    "frameId": frame_id,
                }
            )

    orphaned_keys = set(manifest.keys()) - current_keys

    if verify_cache:
        if mismatches or orphaned_keys:
            print("excalidraw cache is stale:", file=sys.stderr)
            for key in mismatches:
                print(f"  mismatch: {key}", file=sys.stderr)
            for key in sorted(orphaned_keys):
                print(f"  orphaned: {key}", file=sys.stderr)
            sys.exit(1)
        print(f"excalidraw: cache verified, {len(current_keys)} block(s) OK")
        return

    if unresolved:
        print("warning: couldn't resolve these embedded scene links:", file=sys.stderr)
        for link_target in unresolved:
            print(f"  {link_target}", file=sys.stderr)
    if missing_frames:
        print("warning: referenced frame(s) not found in their scene:", file=sys.stderr)
        for ref in missing_frames:
            print(f"  {ref}", file=sys.stderr)

    if dry_run:
        elapsed = time.time() - start
        print(
            f"excalidraw (dry-run): {len(references)} embed(s), {n_blocks} block(s) referenced, "
            f"{len(miss_jobs)} would-render, {len(papers_miss_jobs)} papers-json would-write, "
            f"{len(hit_keys)} cached, {len(orphaned_keys)} orphaned, {elapsed:.1f}s"
        )
        if miss_jobs:
            print("would render:", file=sys.stderr)
            for job in miss_jobs:
                print(f"  {job['key']}", file=sys.stderr)
        if papers_miss_jobs:
            print("would write (papers json):", file=sys.stderr)
            for job in papers_miss_jobs:
                print(f"  {job['key']}", file=sys.stderr)
        if orphaned_keys:
            label = "would remove (--prune-orphans)" if prune_orphans else "found, not removed"
            print(f"orphaned ({label}):", file=sys.stderr)
            for key in sorted(orphaned_keys):
                print(f"  {key}", file=sys.stderr)
        return

    results = run_render_batch(miss_jobs)
    rendered_keys = set()
    failed = []
    for result in results:
        if result.get("ok"):
            rendered_keys.add(result["key"])
        else:
            failed.append(result)

    job_by_key = {job["key"]: job for job in miss_jobs}
    for key in rendered_keys:
        job = job_by_key[key]
        rel_out = os.path.relpath(job["outputPath"])
        digest = block_hash(job["elements"], job["appState"])
        manifest[key] = {"hash": digest, "svg": rel_out, "frameId": job["frameId"]}

    for job in papers_miss_jobs:
        payload = {"elements": job["elements"], "appState": job["appState"], "files": job["files"]}
        with open(job["path"], "w", encoding="utf-8") as f:
            json.dump(payload, f, sort_keys=True)
            f.write("\n")
        manifest[job["key"]] = {"hash": job["digest"], "papersJson": os.path.relpath(job["path"])}

    # Orphans (previously rendered, no longer referenced by anything) are
    # never deleted automatically -- a run of this script shouldn't be able
    # to make files disappear as a side effect. Report them; deletion only
    # happens if you explicitly ask for it with --prune-orphans.
    if orphaned_keys and not prune_orphans:
        print(f"orphaned (not removed -- rerun with --prune-orphans to clean up): {len(orphaned_keys)}", file=sys.stderr)
        for key in sorted(orphaned_keys):
            entry = manifest.get(key)
            out_path = entry.get("svg") or entry.get("papersJson") if isinstance(entry, dict) else None
            print(f"  {key}" + (f" -> {out_path}" if out_path else ""), file=sys.stderr)

    pruned = 0
    if prune_orphans:
        for key in orphaned_keys:
            entry = manifest.pop(key, None)
            out_path = entry.get("svg") or entry.get("papersJson") if isinstance(entry, dict) else None
            if out_path and os.path.exists(out_path):
                os.unlink(out_path)
                print(f"orphaned: removed {out_path} ({key})", file=sys.stderr)
            else:
                print(f"orphaned: removed stale manifest entry ({key})", file=sys.stderr)
            pruned += 1

    save_manifest(manifest)

    if failed:
        print("render failures:", file=sys.stderr)
        for result in failed:
            print(f"  {result['key']}: {result.get('error')}", file=sys.stderr)

    elapsed = time.time() - start
    print(
        f"excalidraw: {len(references)} embed(s), {n_blocks} block(s) referenced, "
        f"{len(rendered_keys)} rendered, {len(hit_keys)} cached, {elapsed:.1f}s"
        + (f" ({len(failed)} failed)" if failed else "")
        + (f" ({pruned} orphaned removed)" if pruned else "")
        + (f" ({len(orphaned_keys)} orphaned, not removed)" if orphaned_keys and not prune_orphans else "")
    )
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
