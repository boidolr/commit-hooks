.DEFAULT_GOAL := all


# venv handling: https://github.com/sio/Makefile.venv/blob/master/Makefile.venv
VENVDIR=.venv
MARKER=.initialized-with-Makefile.venv
VENV=$(VENVDIR)/bin


$(VENV):
	python3 -m venv $(VENVDIR)
	$(VENV)/python3 -m pip install --upgrade pip setuptools wheel


$(VENV)/$(MARKER): $(VENV)


## venv        : Initialize virtual environment with dependencies.
.PHONY: venv
venv: $(VENV)/$(MARKER)
	$(VENV)/pip install -q -r requirements.txt -r requirements-dev.txt


.PHONY: all
all: sync format check test version


.PHONY: help
help: Makefile
	@sed -n 's/^##//p' $< | sort


## sync        : Update yaml versions from requirements file.
.PHONY: sync
sync: requirements.txt
	python3 build/sync_versions.py $< setup.cfg .pre-commit-hooks.yaml


## upgrade     : Update pre-commit configuration.
.PHONY: upgrade
upgrade: venv
	$(VENV)/pre-commit autoupdate


## check       : Execute pre-commit hooks.
.PHONY: check
check: venv
	$(VENV)/pre-commit run --all-files


## format      : Format code.
.PHONY: format
format: venv
	$(VENV)/black -q .


## test        : Execute tests.
.PHONY: test
test: venv
	$(VENV)/pytest -q


## version     : Show which version is detected and what the next one would be.
CURRENT:=$(subst v,,$(shell git describe --abbrev=0 --tags))
PARTS:=$(subst ., ,$(CURRENT))
MAJOR:=$(firstword $(PARTS))
MINOR:=$(shell echo $$(($(lastword $(PARTS))+1)))
VERSION:=$(MAJOR).$(MINOR)
.PHONY: version
version:
	@echo "Version update: $(CURRENT) -> $(VERSION)"


## release     : Increase version in files, commit and tag with git.
.PHONY: release
release: test version
	@sed  -E -e "s/rev: v${CURRENT}/rev: v${VERSION}/" -i '' README.md
	@sed  -E -e "s/version = ${CURRENT}/version = ${VERSION}/" -i '' setup.cfg
	@git add README.md setup.cfg
	git commit -m "Release version ${VERSION}" && git tag "v${VERSION}"


## clean       : Remove virtual environment.
.PHONY: clean
clean:
	rm -r "$(VENVDIR)"
