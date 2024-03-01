py-linux-template
==============================

**repo-status: work in progress**

This is a template for a python project on linux.

The following files are included in this template:

0. [Project structure](docs/project_structure.md) to view the structure of this template.

1. **Makefile** to setup and configure your project

2. Configuration files:
    - [config.yaml](config/config.yaml) to set your project configuration
    - [template.env](config/template.env) to set your environment variables
    - [logging.yaml](config/logging.yaml) to set your logging configuration
    - [pyproject.toml](pyproject.toml) to set your project dependencies.
    - [pre-commit-config.yaml](pre-commit-config.yaml) to set your pre-commit hooks.

3. Python files:
    - [config.py](src/config.py) to load your project configuration.
    - [logger.py](src/logger.py) to set up your logging configuration.
    - [utils.py](src/utils.py) project utility methods.
    - [decorators.py](src/decorators.py) project decorators.

6. A sample project to test the *src package* in this template ([here](sample_project/main.py)).

5. A test-suite using the pytest framework to test the *src package* in this template ([here](tests/test_utils.py)).

6. Documentation:
    - [linux shell cheatsheet](docs/cheatsheet_linux_shell.md)  overview of shell commands.
    - [linux set up document](docs/linux_set_up.md) for a detailed description of different tools and how to publish your package.

-------

## Set up and configure your project

1. Click on the green button "Use this template" on GitHub.
2. Open VS Code and clone the repository.
3. Install the project dependencies:
    - `make help` to see the available commands.
    - `make install-global` to install packages such as pre-commit, poetry, and black globally using pipx.
    - `make poetry-install` to install the project dependencies (creates poetry.lock)
4. Set the Python Interperater to the poetry virtual environment.
    - Select Interpreter *project-name-xxxxx-py.x.xx (poetry)*
5. Set up the configuration files:
    - check your project configuration: [config.yaml](config/config.yaml)
    - set your environment variables: [template.env](config/template.env) (rename to .env, do not commit to git!!)
    - check your logging configuration: [logging.yaml](config/logging.yaml)
6. Set up linting and pre-commit hooks:
    - `make codestyle` to run black, isort and ruff.
    - `make pre-commit` to run pre-commit on all files.
7. Run the tests:
    - `make poetry-test` to run all tests.
    - Run from VS Code: testing > configure python tests > pytest
8. Run pre-commit hooks and commit your changes:
    - `git add .` to add all files to the staging area.
    - `make pre-commit` to run pre-commit on all files.
    - `git commit -m "commit message"` to commit your changes.

9. Publish your package to PyPI:
    - See the [linux set up document](docs/linux_set_up.md) for a detailed description of different tools and how to publish your package.


### Workflow






### References
-
-

### Citation

### Acknowledgments

*This repository is part of the project:*

** xxxx Project** | Long name project.
