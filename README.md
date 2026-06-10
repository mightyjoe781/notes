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

## Linting

```bash
vale docs/    # prose lint (custom + Microsoft style, see .vale.ini)
```
