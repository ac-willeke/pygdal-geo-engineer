# Linux Set Up for Python Development
This document describes how to set up a Linux environment for Python development. The information is based on the documentation from [Python Packages](https://py-pkgs.org/welcome),  [DataCamp](https://www.datacamp.com) course material and [Packaging for Python](https://packaging.python.org/en/latest/tutorials/packaging-projects/). See the [cheatsheet](cheatsheet_unix_shell.md) for a quick overview of the Unix shell.


## Installation

Check your shell configuration using the command `echo $0`.

### 1. Python

 - Check if and where Python is installed.

      ```bash
      # Standard Python Distribution
      which python3
      python3 --version
      which pip
      which pipx

      # Anaconda Distribution
      which conda
      conda --version
      ```


- Standard Python distribution

   - download and install from [python.org](https://www.python.org/downloads/)

   - add Python to your PATH
   - Install `pipx`: `python3 -m pip install pipx`
   - Configure PATH: `pipx ensurepath`
   - Close and open your shell again



- Miniconda distribution
   - download and install from [conda.io](https://docs.conda.io/en/latest/miniconda.html)

      ```bash
      # create a directory
      mkdir -p ~/miniconda3
      cd miniconda3

      # download miniconda
      wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

      # rename file to miniconda.sh
      mv Miniconda3-latest-Linux-x86_64.sh miniconda.sh

      # install miniconda
      bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3

      # remove installation file
      rm -rf ~/miniconda3/miniconda.sh
      ``````
   - initialize conda

      ```bash
      ~/miniconda3/bin/conda init
      ```
   - close and re-open your shell
   - ensure that conda is up to date `conda update --all`


| Python Distribution | Python Path | Python Version |
| ------------------- | ----------- | -------------- |
|standard distribution| `/usr/bin/python3` | `Python 3.10.12` |
|miniconda distribution| `/home/username/miniconda3/bin/conda/` | `conda 23.5.2`


## 2. Git and Github

- install git: [git-scm.com](https://git-scm.com/download/linux)
- login to GitHub in vscode
- configure git
   ```shell
   git config --global user.name "John Doe"
   git config --global user.email johndoe@example.com
   git config --global init.defaultBranch main

   # check your settings
   git config --list --show-origin
   ```
- create `.gitignore` and add files and directories that should not be tracked by git

## 3. Register for a PyPI account
The Python Package Index (PyPI) is the official online software repository for Python. A software repository is a storage location for downloadable software, like Python packages. Before publishing packages to PyPI, it is typical to “test drive” their publication on TestPyPI, which is a test version of PyPI. It is recommended to register for a TestPyPI account on the TestPyPI website and a PyPI account on the PyPI website.

- Test PyPI: [test.pypi.org](https://test.pypi.org/account/register/)
- PyPI: [pypi.org](https://pypi.org/account/register/)

## 4. Pre-commit
** pre-commit** checks certain actions before committing changes to your repository. The list of actions that are executed are defined in `.pre-commit-config.yaml`.
   - Install `pre-commit`: `pipx install pre-commit`
   - Enter into your git repository and install the hooks: `pre-commit install` (optional, but recommended)
   - de-activate pre-commit:
      - delete or comment out the lines in .pre-commit-config.yaml
      - `pre-commit uninstall`
      - `pre-commit clean`

**How to use pre-commit:**

In case you executed `pre-commit install`, `pre-commit` hooks will be executed each time you will try to commit (`git commit`). If any of the checks fail or if any files that is going to be committed is changed (because a tool refactored or cleaned it), the commit will fail.

The suggested method to use `pre-commit` is to run it before trying to commit your changes, using `pre-commit run -a`. You can run this command multiple times, to check if the changes are ready to be committed.
After all the tests succeeded, the changes can be staged (`git add`) and committed.

**Note**: Solely install pre-commit in the standard distribution, not in the miniconda distribution or project-specific poetry environment.

## 4. Project Structure

The project structure of this template is shown [here](project_structure.md). You can use this repository as a template for your own project or create a project structure using `cookiecutter`.

```shell
which cookiecutter
cd path/to/your/project
cookiecutter <path/to/cookiecutter/template>
```

Templates:
- [cookiecutter-data-science](https://github.com/drivendata/cookiecutter-data-science)
- [python-package-template](https://github.com/TezRomacH/python-package-template)
- [cookiecutter] (https://github.com/py-pkgs/py-pkgs-cookiecutter.git)

In Visual Studio Code you can use the default extension `vscode-cookierunner` to define default cookiecutter templates.



## 5. Poetry

Poetry is a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you. Poetry also allows you to create a virtual environment for your project, so that your project is isolated from your system.

- documentation: [poetry-docs](https://python-poetry.org/docs/)

- install poetry: `pipx install poetry` or `make install-poetry`

**Configuration files:**
- `pyproject.toml`: contains project information and its dependencies. project, including its dependencies. Documentation [here](https://python-poetry.org/docs/pyproject/).
- `poetry.lock`: contains the exact versions of the dependencies that were installed in your project.

The `poetry.lock` file is automatically generated and should not be edited. It contains the exact versions of the dependencies that were installed in your project.

**Poetry set-up in VS Code:**
- install poetry extension in VS Code
- activate poetry environment in terminal: `poetry shell`
- set the Python Environment (bottom-left corner) to the poetry environment

## 4. Code Formatters and Linter
In this template the following code formatters and linter are used:

- [Black](https://black.readthedocs.io/en/stable/) (code formatter)

- [Isort](https://pycqa.github.io/isort/) (sorts imports)

- [Ruff](https://github.com/astral-sh/ruff) (linter)

- [pyment](https://github.com/dadadel/pyment) (docstring formatter), docstrings in this template use the Numpy style.

Example of a docstring in Numpy style for a function:

```python
class Vehicles(object):
    '''
    The Vehicles object contains lots of vehicles

    Parameters
    ----------
    arg : str
        The arg is used for ...
    *args
        The variable arguments are used for ...
    **kwargs
        The keyword arguments are used for ...

    Attributes
    ----------
    arg : str
        This is where we store arg,
    '''
    def __init__(self, arg, *args, **kwargs):
        self.arg = arg

    def cars(self, distance, destination):
        '''We can't travel distance in vehicles without fuels, so here is the fuels

        Parameters
        ----------
        distance : int
            The amount of distance traveled
        destination : bool
            Should the fuels refilled to cover the distance?

        Raises
        ------
        RuntimeError
            Out of fuel

        Returns
        -------
        cars
            A car mileage
        '''
        pass

```

Example of a docstring in reStructured text style for a function:

```python
"""Summary line.

Extended description of function.

:param arg1: Description of arg1
:type arg1: int
:param arg2: Description of arg2
:type arg2: str
:returns: Description of return value
:rtype: bool
:raises ValueError: if `param2` is equal to `param1`.
```

The configuration for these tools is set in the `pyproject.toml` file.

## 7. Makefile

*Make* is a tool that is used for automating tasks by defining a set of instructions in a `Makefile` which is located in your projects root directory. Install make using: `sudo apt install make`

Good practices in Makefiles:
- testing, cleaning targts should be phony.
- environment setup (like tool installation) targets do not need to be phony.
- define a single .PHONY at the top of the Makefile
- group targets by functionality

A template Makefile is provided in this repository. It contains the following targets:
- `make global-install`: installs all dependencies that are not project-specific using pipx
   - pre-commit
   - black
   - isort
   - ruff
   - pyment

- `make poetry-install`: installs all dependencies that are project-specific using poetry
- `make codestyle`: runs all code quality checks (black, isort, ruff, pyment)
- `make docstring`: generates or converts docstrings to the reStructured text style using pyment
- `make cleanup`: removes all temporary files and directories

## 8. Gdal and Geospatial Libraries

*Why is it better to install gdal using pip instead of conda?*
- [doc](https://towardsdev.com/why-would-you-install-gdal-using-pip-not-conda-ad83f0b0c370)
- Conda requires a lot of storage space
   - it installs a lot of standard dependencies
   - conda pacagkes are binaries and do not need to be compiled
- Conda not suitable for CI/CD pipelines and github actions as the performance is very slow

Install gdal using conda:
```shell
conda install -c conda-forge gdal
```

Install gdal using pip:
[doc](https://towardsdev.com/gdal-installation-for-linux-b15faf5eb74b)
```shell
   which python3 # 3.10.12
   which gcc -v # 11.4.0
   which g++ -v # 11.4.0

   sudo apt-get update # update the package index
   sudo apt-get upgrade # upgrade the system
   sudo apt-get -y install gcc g++ # install gcc and g++ compilers (required to compile python extensions)
   sudo add-apt-repository ppa:deadsnakes/ppa # add deadsnakes repository to apt sources list  (deadsnakes contains python)
   sudo apt -y install python3.10
   sudo apt-get -y install python3-pip
   sudo apt-get -y install python3.10-distutils python3-apt
   sudo apt-get -y install python3.10-dev
   sudo apt-add-repository ppa:ubuntugis/ubuntugis-unstable # add ubuntugis repository to apt sources list (ubuntugis contains gdal)

   sudo apt search gdal-bin # search for gdal-bin in the apt repository
   sudo apt-get install gdal-bin
   sudo apt-get -y install libpq-dev libgdal-dev

```

Packages
========

The packages provided here are loosely based on the debian upstream packages with some modifications to make them more usable as non-default pythons and on ubuntu. As such, the packages follow debian's patterns and often do not include a full python distribution with just `apt install python#.#`. Here is a list of packages that may be useful along with the default install:

- `python#.#-dev`: includes development headers for building C extensions
- `python#.#-venv`: provides the standard library `venv` module
- `python#.#-distutils`: provides the standard library `distutils` module
- `python#.#-lib2to3`: provides the `2to3-#.#` utility as well as the standard library `lib2to3` module
- `python#.#-gdbm`: provides the standard library `dbm.gnu` module
- `python#.#-tk`: provides the standard library `tkinter` module

# Create, Build and Publish a Python Package

## 1. Create a Python Package
*Based on tutorial from [Packaging for Python](https://packaging.python.org/en/latest/tutorials/packaging-projects/)*


   1. Create the **directory structure**:
      - create a directory for your package (manual or by using template, e.g. `poetry new --src my-package`, cookiecutter or github template)
      - create a 'src' directory that contains your package, subpackages and modules, with a `__init__.py` file that marks the directory as a Python package.

      ```shell
      # example
      ├── src
      │   ├── __init__.py
      │   ├── sub-package1
      │   │   ├── __init__.py
      │   │   └── module1.py
      │   ├── sub-package2
      │   │   ├── __init__.py
      │   │   └── module2.py
      │   └── module3.py


      # poetry new example
      my-package
      ├── pyproject.toml
      ├── README.md
      ├── src
      │   └── my_package
      │       └── __init__.py
      └── tests
         └── __init__.py
      ```
   2. Create the **package distruibution files**
      - create `tests` directory for test files.
      - create `pyproject.toml` configuration. It tells build-tools like poetry, flit, setuptools-scm, etc. how to build a distribution form your package.
         - Build System Configurations: [build-system]
         - Project Configurations: [tool.poetry] or [project]
         - Dependency Configurations: [tool.poetry.dependencies] or [project]
         - Development Dependency Configurations (Poetry Group): [tool.poetry.dev-dependencies]
         - Specific Tool Configurations: [tool.black], [tool.isort], [tool.ruff], [tool.pyment]
      - create README.md
      - create license file

   **NOTE: pyproject.toml vs setup.py**

   *`pyproject.toml` is the new standard for packaging Python projects. It contains the metadata and configuration for build tools like poetry, flit and setuptools-scm to setup your project. [build-system] defines which build tool is used.*

   ```bash
   # install dependencies using poetry
   # your local package is installed in editable mode
   poetry install
   ```
   *`setup.py` and `requirements.txt` is the old standard.The setup.py script contains the metadata for your project and reads the package requirements from your txt file.*

   ```bash
   # install dependencies using setuptools
   # your local package is installed in editable mode

   # activate env
   source venv/bin/activate

   python setup.py install -e.
   # or
   pip install -e .
   ```

## 2. Build the package distribution

   Distribution packages are archives that are uploaded to the Python Package Index and which can be installed by pip.

   - source archives (sdists)
   - wheels (bdist_wheel)

   **recommended packaging tools**:
   - poetry, recommended for developing "pure" Python packages.
   - setuptools, recommended for developing more advanced Python packages that might include C extensions or other non-Python code.

   ```shell
   # build using poetry
   poetry build

   # build using setuptools
   python3 -m pip install --upgrade build
   python3 -m build

   # output
   dist/
   ├── my_package-0.0.1-py3-none-any.whl
   └── my_package-0.0.1.tar.gz
   ```

## 3. Publish the package distribution

Upload your package distribution archives to Python Package Index (PyPI) or TestPyPI. Twine and Poetry are recommended tools for uploading.

- install Twine: `pipx install twine`
- create a (test)PyPI API token. The token is used to authenticate your package uploads. You can create a token on the [PyPI website](https://pypi.org/manage/account/token/) and save it in a secure place (e.g. .env file)
   **scope = Entire account*
- configure your twine or poetry settings
   - twine: create a .pypirc file with your API-key information
   - poetry: `poetry config pypi-token.pypi <your-token>`
- upload your package to PyPI or TestPyPi
   ```shell
   # upload using twine
   python3 -m twine upload --repository testpypi dist/*

   # upload using poetry
   poetry publish -r testpypi
   ```

## 4. Install the package (TODO)

# Publish Documentation (TODO)
##  Compile the documentation (TODO)
https://packaging.python.org/en/latest/tutorials/creating-documentation/
https://py-pkgs.org/06-documentation/

# Testing (TODO)
- Unit Tests
exampole of unit tests for the config and utils modules are included here.

run the test with make using `make poetry-test` for a poetry env or `make test` for a venv.

TODO: one test shows 33% coverage, when all tests are run but 100% if only the test for the config module is run.



# Continuous Integration (TODO)

## 1. Update the package (TODO)
- using git messages (semantic versioning) DO after trekroner is fully tested and you published first version to PyPI.

## 2. Versioning

## 3. Continuous Integration and Deployment

# GitHub Actions (TODO)
- search python

# Envrioment Variables in Linux shell (TODO)
https://github.com/mkaranasou/pyaml_env
https://medium.com/swlh/python-yaml-configuration-with-environment-variables-parsing-77930f4273ac

## References

- [Python Packages](https://py-pkgs.org/welcome)
- [Python](https://docs.python.org/3/)
- [Git](https://git-scm.com/doc)
- [GitHub](https://docs.github.com/en)
- [PyPI](https://pypi.org/help/)
- [Poetry](https://python-poetry.org/docs/)
- [Make](https://www.gnu.org/software/make/manual/make.html)
- [Pre-commit](https://pre-commit.com/)
- [Black](https://black.readthedocs.io/en/stable/)
- [Isort](https://pycqa.github.io/isort/)
- [Ruff](https://github.com/astral-sh/ruff)
- [pyment](https://github.com/dadadel/pyment)
