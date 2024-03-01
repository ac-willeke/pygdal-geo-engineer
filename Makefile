.PHONY: codestyle formatting docstring pre-commit clean clean-venv clean-build clean-pyc clean-linting clean-test clean-log poetry-clean

.DEFAULT_GOAL := help
SHELL := /bin/bash
VENV_NAME := .venv

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python3 -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

# --------------------------------------------------------------------------- #
# Style targets
# --------------------------------------------------------------------------- #

codestyle: ## check codestyle (black, isort, ruff)
	isort --settings-path pyproject.toml ./
	black --config pyproject.toml ./
	ruff check ./

docstring: ## create/ update docstring to restructured text
	pyment -w -o numpydoc ./
#pyment -w -o reST ./
#pyment -w -o google ./

pre-commit: ## run pre-commit on all files
	pre-commit run -a
#pre-commit run -a --config config/.pre-commit-config.yaml

# --------------------------------------------------------------------------- #
# Cleaning targets
# --------------------------------------------------------------------------- #

clean: clean-venv clean-build clean-pyc clean-linting clean-test ## remove all build, test, coverage and Python artifacts

clean-venv: ## remove virtual environment
	rm -rf $(VENV_NAME)

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '.ipynb_checkpoints' -exec rm -fr {} +

clean-linting: ## remove linting artifacts
	find . -name '.ruff_cache' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -fr .pytest_cache

clean-log: ## remove log files in /log folder
	rm -fr log/*.log

# --------------------------------------------------------------------------- #
# Testing targets
# --------------------------------------------------------------------------- #

test: install ## run tests quickly with the virtual environment's Python
	source $(VENV_NAME)/bin/activate
	pytest

test-all: install ## run tests on every Python version with tox
	source $(VENV_NAME)/bin/activate
	tox

# --------------------------------------------------------------------------- #
# Setuptools targets (use on windows or when you have non-python files)
# --------------------------------------------------------------------------- #

venv: clean
	python3 -m venv $(VENV_NAME)

build: clean ## builds source and wheel package
	python3 setup.py sdist
	python3 setup.py bdist_wheel
	ls -l dist

release: clean build ## package and upload a release
	twine upload dist/*

install: venv ## install the packages in requirements.txt in the virtual environment
	source $(VENV_NAME)/bin/activate
	python setup.py install

# --------------------------------------------------------------------------- #
# Poetry targets (use on linux)
# TODO poetry-install-standard is redundant
# --------------------------------------------------------------------------- #

poetry-init: clean ## init poetry in existing project
	poetry init

poetry-install: clean ## install poetry dependencies listed in pyproject.toml
	poetry install

poetry-install-standard: ## install standard poetry dependencies
	poetry add python-dotenv
	poetry add pyaml_env
	poetry add pytest --group dev
	poetry add black --group dev
	poetry add isort --group dev
	poetry add ruff --group dev
	poetry add pyment --group dev

poetry-build: clean ## build python wheels using poetry
	poetry build
	ls -l dist

poetry-release: ## publish python wheels using poetry
	poetry publish --build

poetry-test: poetry-install ## run tests using poetry
	poetry run pytest

poetry-test-all: poetry-install ## run tests on every Python version with tox
	poetry run tox



poetry-clean:
	poetry env remove --all
	rm -f poetry.lock
	@echo "Poetry environment and poetry.lock have been removed."


# --------------------------------------------------------------------------- #
# Installation targets using pipx
# --------------------------------------------------------------------------- #

install-global: install-poetry install-twine install-pre-commit install-black install-isort install-ruff install-pyment install-cookiecutter install-pytest## install global tools

install-poetry: ## install poetry
	pipx install poetry

install-twine: ## install twine
	pipx install twine

install-pre-commit: ## install pre-commit
	pipx install pre-commit

install-black: ## install black
	pipx install black

install-isort: ## install isort
	pipx install isort

install-ruff: ## install ruff
	pipx install ruff

install-pyment: ## install pyment
	pipx install pyment

install-cookiecutter: ## install cookiecutter
	pipx install cookiecutter

install-pytest: ## install pytest
	pipx install pytest
