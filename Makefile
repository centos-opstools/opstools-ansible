DEFAULTS = $(shell find roles -path '*/defaults/main.yml')
READMES = $(shell find roles -name README.md)
PANDOC_EXTENSIONS = yaml_metadata_block+auto_identifiers+implicit_header_references

MARKDOWN = README.md
HTML = $(MARKDOWN:.md=.html)

all: $(MARKDOWN) $(HTML)

README.md: $(DEFAULTS) $(READMES) docs/header.md docs/footer.md
	(cat docs/header.md && \
	python tools/extract-role-docs.py && \
	cat docs/footer.md) > $@ || rm -f $@

README.html: README.md docs/metadata.yml
	pandoc -f markdown+$(PANDOC_EXTENSIONS) \
	docs/metadata.yml README.md -o $@ \
	--standalone --toc --toc-depth 2

clean:
	rm -f $(MARKDOWN) $(HTML)
