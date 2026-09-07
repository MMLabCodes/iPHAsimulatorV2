SPHINXBUILD ?= sphinx-build
SOURCEDIR = .
BUILDDIR = _build

.PHONY: html linkcheck clean
html:
	$(SPHINXBUILD) -b html -W --keep-going $(SOURCEDIR) $(BUILDDIR)/html

linkcheck:
	$(SPHINXBUILD) -b linkcheck $(SOURCEDIR) $(BUILDDIR)/linkcheck

clean:
	$(SPHINXBUILD) -M clean $(SOURCEDIR) $(BUILDDIR)
