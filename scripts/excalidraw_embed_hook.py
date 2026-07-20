#!/usr/bin/env python3
"""MkDocs build hook: resolve Obsidian's native Excalidraw embed syntax into
its rendered SVG, in memory, during the build -- the .md source on disk is
never touched.

Two forms (as authored in Obsidian, see docs/tmp/scratch.md), with or
without the ".md" extension (Obsidian lets you drop it on wikilinks to
markdown files):
    ![[scene.excalidraw]]  /  ![[scene.excalidraw.md]]           whole scene
    ![[scene.excalidraw#^frame=<frameId>]]                       just that Frame
    ![[scene.excalidraw#^frame=<frameId>|<width>]]                ... with a width

become, only in the markdown mkdocs actually converts to HTML:
    ![](relative/path/to/scene.excalidraw.svg)
    ![](relative/path/to/scene.excalidraw__<name>.svg)
    ![](relative/path/to/scene.excalidraw__<name>.svg){: width="<width>" }

This is deliberately non-destructive: you keep editing the wikilink form in
Obsidian (live Excalidraw preview stays intact), and you can repoint a note
at a different frame -- or drop the frame reference entirely to fall back to
the whole scene -- at any time; the next build just picks it up.

scripts/render_excalidraw.py is what actually renders scenes/frames to SVG
and writes docs/.excalidraw-manifest.json; this hook only reads that
manifest to resolve embeds to SVG paths. It never renders anything itself.
To keep `mkdocs serve`'s live-reload useful (editing a scene's content
should update the page without a full restart), on_pre_build below re-runs
render_excalidraw.py before every build -- including every incremental
rebuild the serve watcher triggers, not just the first one. It's a fast
no-op (reference-driven + content-hash cached) when nothing changed, so
this doesn't meaningfully slow down local iteration.

If a scene hasn't been rendered yet, or a referenced frame no longer
exists, the embed is left untouched rather than breaking the build.

Wired in via the `hooks:` key in mkdocs.yml and mkdocs_local.yml.
"""

import json
import os
import re
import subprocess
import sys

DOCS_DIR = "docs"
MANIFEST_PATH = os.path.join(DOCS_DIR, ".excalidraw-manifest.json")
RENDER_SCRIPT = os.path.join("scripts", "render_excalidraw.py")

# The #^frame=<id> anchor is optional -- a bare ![[scene.excalidraw]] means
# "the whole scene" (the "default" block render_excalidraw.py always
# produces). The ".md" extension is optional too, same as any Obsidian
# wikilink to a markdown file -- kept in sync by hand with the identical
# pattern in scripts/render_excalidraw.py (that script decides what needs
# rendering in the first place; this one only resolves already-rendered
# paths).
EMBED_RE = re.compile(r"!\[\[([^\]|#]+\.excalidraw)(?:\.md)?(?:#\^frame=([^\]|]+))?(?:\|(\d+))?\]\]")

# {(scene_path, frame_id_or_None): svg_path}, both relative to repo root.
# frame_id is None for the whole-scene "default" block.
_frame_index: dict[tuple[str, str | None], str] | None = None


def _load_frame_index() -> dict[tuple[str, str | None], str]:
    global _frame_index
    if _frame_index is not None:
        return _frame_index

    _frame_index = {}
    if not os.path.exists(MANIFEST_PATH):
        return _frame_index

    with open(MANIFEST_PATH, encoding="utf-8") as f:
        manifest = json.load(f)

    for key, entry in manifest.items():
        if not isinstance(entry, dict):
            continue
        scene_path = key.split("::", 1)[0]
        svg_path = entry.get("svg")
        if svg_path:
            _frame_index[(scene_path, entry.get("frameId"))] = svg_path

    return _frame_index


def on_pre_build(config, **kwargs):
    """Runs before every build, including each rebuild `mkdocs serve`'s
    watcher triggers on a file change -- not just the first one. Without
    this, editing a scene mid-`serve` would never re-render (the manifest
    only updates when render_excalidraw.py is explicitly run), and only a
    full restart would pick the change up."""
    global _frame_index
    _frame_index = None  # the manifest this build should read is about to change

    proc = subprocess.run(
        [sys.executable, RENDER_SCRIPT],
        capture_output=True,
        text=True,
    )
    if proc.stdout.strip():
        print(proc.stdout.strip())
    if proc.returncode != 0:
        print(f"warning: {RENDER_SCRIPT} exited {proc.returncode}", file=sys.stderr)
        if proc.stderr.strip():
            print(proc.stderr.strip(), file=sys.stderr)


def on_page_markdown(markdown, page, config, files, **kwargs):
    if "![[" not in markdown or ".excalidraw" not in markdown:
        return markdown

    frame_index = _load_frame_index()
    # page.file.src_uri is the page's path relative to docs_dir, e.g. "tmp/scratch.md"
    doc_dir = os.path.join(DOCS_DIR, os.path.dirname(page.file.src_uri))

    def replace(match: re.Match) -> str:
        link_target, frame_id, width = match.group(1), match.group(2), match.group(3)
        suffix = link_target + ".md"

        # Resolution order matches scripts/render_excalidraw.py's
        # resolve_scene_path: relative to this page's own directory first
        # (handles "../"-style relative links, Obsidian's "relative path to
        # file" format), then vault-root-relative, then a shortest-path
        # suffix match.
        relative_to_page = os.path.normpath(os.path.join(doc_dir, suffix))
        relative_to_docs_root = os.path.normpath(os.path.join(DOCS_DIR, suffix))

        svg_path = frame_index.get((relative_to_page, frame_id))
        if svg_path is None:
            svg_path = frame_index.get((relative_to_docs_root, frame_id))
        if svg_path is None:
            candidates = [
                svg for (sp, fid), svg in frame_index.items() if fid == frame_id and sp.endswith(suffix)
            ]
            svg_path = candidates[0] if len(candidates) == 1 else None

        if svg_path is None:
            # Not rendered (yet) -- leave the embed as-is rather than
            # breaking the build with a dead link.
            return match.group(0)

        rel = os.path.relpath(svg_path, doc_dir)
        if width:
            return f'![]({rel}){{: width="{width}" }}'
        return f"![]({rel})"

    return EMBED_RE.sub(replace, markdown)
