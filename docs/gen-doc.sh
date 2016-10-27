#!/bin/sh

cd $(git rev-parse --show-toplevel)

(
cat docs/header.md
python docs/extract-role-docs.py
cat docs/footer.md
) |
tee README.md |
pandoc -f markdown+pandoc_title_block \
	--toc --toc-depth 2 \
	-o README.html --standalone
