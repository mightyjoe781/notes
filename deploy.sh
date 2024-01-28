#!/bin/sh
mkdocs build && rsync -avz --delete site/ mtboxroot:/var/www/notes/
exit 0
