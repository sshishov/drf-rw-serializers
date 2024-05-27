.PHONY: clean compile_translations coverage docs dummy_translations \
	extract_translations fake_translations help pull_translations push_translations \
	quality requirements selfcheck test test-all upgrade validate

.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help: ## display this help message
	@echo "Please use \`make <target>' where <target> is one of"
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

clean: ## remove generated byte code, coverage reports, and build artifacts
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	poetry run coverage erase
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

coverage: clean ## generate and view HTML coverage report
	poetry run pytest --cov-report html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/drf-rw-serializers.rst
	rm -f docs/modules.rst
	poetry run sphinx-apidoc -o docs/ drf_rw_serializers
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html


upgrade: ## update the dependencies in pyproject.toml with the latest versions
	poetry update

quality: ## check coding style with pycodestyle and pylint
	poetry run tox -e quality

requirements: ## install development environment requirements
	poetry install

test: clean ## run tests in the current virtualenv
	poetry run pytest

diff_cover: test
	poetry run diff-cover coverage.xml

test-all: ## run tests on every supported Python/Django combination
	poetry run tox -e quality
	poetry run tox

validate: quality test ## run tests and quality checks

selfcheck: ## check that the Makefile is well-formed
	@echo "The Makefile is well-formed."

release: clean ## package and upload a release
	poetry build
	poetry run twine check dist/*
	poetry run twine upload dist/*

sdist: clean ## package
	poetry build
	ls -l dist
