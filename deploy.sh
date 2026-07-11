#!/bin/sh

# Activate Python virtual environment if not already activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    if [[ -f "venv/bin/activate" ]]; then
        source venv/bin/activate
    elif [[ -f ".venv/bin/activate" ]]; then
        source .venv/bin/activate
    fi
fi

mkdocs build
python3 scripts/generate_llms_txt.py
rsync -avz --delete site/ smkroot:/var/www/notes/
exit 0
