#!/usr/bin/env bash

# Activate Python virtual environment if not already activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    if [[ -f "venv/bin/activate" ]]; then
        source venv/bin/activate
    elif [[ -f ".venv/bin/activate" ]]; then
        source .venv/bin/activate
    fi
fi

# mkdocs serve -f mkdocs_local.yml "$@" &> /dev/null
mkdocs serve -f mkdocs_local.yml -q
