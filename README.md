# smk's notes

Personal knowledge base built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/). Live at <https://notes.sudomoon.com/>.

## Structure

- `docs/` - markdown content + assets, organized by topic
- `mkdocs.yml` / `mkdocs_local.yml` - production / local dev config
- `overrides/` - Material theme template overrides
- `collect.py` - bundles docs per topic into `split/` for LLM context

## Local dev

```bash
source .venv/bin/activate
./serve.sh    # http://127.0.0.1:8000
```

## Deploy

```bash
./deploy.sh   # mkdocs build + rsync to remote server
```

## Excalidraw rendering

`.excalidraw.md` scenes embedded with `![[scene.excalidraw.md]]` or
`![[scene.excalidraw.md#^frame=<id>]]` render to real SVG automatically as
part of `serve.sh`/`deploy.sh` — no manual PNG export needed. See
[`EXCALIDRAW_RENDERING.md`](EXCALIDRAW_RENDERING.md) for how the pipeline
works (embed syntax, caching, the mkdocs hook) and
[`EXCALIDRAW_RENDERING_CHANGELOG.md`](EXCALIDRAW_RENDERING_CHANGELOG.md)
for how it got built.

## Excalidraw library

`docs/Excalidraw/Libraries/local-library.excalidrawlib` is the importable
library file, managed directly by the Obsidian plugin (vault storage mode) -
just commit it after updating the library in Obsidian.

## Linting

```bash
vale docs/    # prose lint (custom + Microsoft style, see .vale.ini)
```
