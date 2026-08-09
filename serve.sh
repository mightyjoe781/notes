#!/usr/bin/env bash

# Activate Python virtual environment if not already activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    if [[ -f "venv/bin/activate" ]]; then
        source venv/bin/activate
    elif [[ -f ".venv/bin/activate" ]]; then
        source .venv/bin/activate
    fi
fi

# python3 scripts/render_excalidraw.py

# Papers viewer JS bundle (scripts/excalidraw-render/src/viewer-entry.js).
# Not wired into the on_pre_build hook like render_excalidraw.py -- it only
# needs rebuilding when that source changes, not on every markdown edit.
# Re-run manually (`npm run build` in scripts/excalidraw-render/) after
# editing it; mkdocs serve's watcher picks up the resulting
# docs/assets/papers/viewer.js change like any other file under docs/.
if [ ! -f docs/assets/papers/viewer.js ]; then
    (cd scripts/excalidraw-render && npm run build)
fi

# mkdocs serve -f mkdocs_local.yml "$@" &> /dev/null
mkdocs serve -f mkdocs_local.yml -q
