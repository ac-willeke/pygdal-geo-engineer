.PHONY: codestyle docstring pre-commit clean clean-venv clean-build clean-pyc clean-linting clean-test clean-log poetry-clean

.DEFAULT_GOAL := help
SHELL := /bin/bash
VENV_NAME := env

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
# Poetry targets (use on linux)
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

poetry-clean:
	poetry env remove --all
	rm -f poetry.lock
	@echo "Poetry environment and poetry.lock have been removed."

install-poetry: ## install poetry
	pipx install poetry

