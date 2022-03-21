#!/bin/sh
mkdocs build && rsync -avz --delete site/ smkroot:/var/www/books/
exit 0
