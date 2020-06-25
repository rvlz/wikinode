.PHONY: test test-all clean clean-pyc clean-test docs

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

clean: clean-pyc clean-build clean-test

clean-pyc: # remove python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/

clean-test: ## remove test artifacts
	rm -fr .tox/

build-env: venv requirements/prod.txt # sync virtual environment
	venv/bin/pip-sync requirements/prod.txt

dev-env: venv requirements/dev.txt # create dev environment
	venv/bin/pip-sync requirements/dev.txt

test:
	python -m pytest

test-all:
	tox

docs:
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/build/html/index.html

dev.txt: requirements/dev.in # development dependencies
	venv/bin/pip-compile -o requirements/dev.txt requirements/dev.in

tests.txt: requirements/tests.in # test dependencies
	venv/bin/pip-compile -o requirements/tests.txt requirements/tests.in

prod.txt: requirements/prod.in # production dependencies
	venv/bin/pip-compile -o requirements/prod.txt requirements/prod.in

docs.txt: requirements/docs.in # docs dependencies
	venv/bin/pip-compile -o requirements/docs.txt requirements/docs.in

dist: clean-build
	python setup.py sdist bdist_wheel

dist-check:
	twine check dist/*

release:
	twine upload dist/*
