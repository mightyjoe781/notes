#!/bin/sh
mkdocs build && rsync -avz --delete site/ smkroot:/var/www/notes/
exit 0
