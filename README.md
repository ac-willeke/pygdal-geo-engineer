PYGDAL-GEO-ENGINEER
==============================

**repo-status: work in progress**

A collection of scripts to perform geospatial engineering tasks using GDAL, Python and SQL. The scripts are organized in a modular way under `src/` and are designed to be run from the command line or within a Jupyter notebook.

## Getting Started 

This project utilizes GDAL, known for its complex installation. To simplify this, a Dockerfile is included, leveraging a GDAL image to run the project within a container. Alternatively, if GDAL bindings are already installed on your machine, the pyproject.toml file can be used to set up a virtual environment.
    
### Virtual Environment 

You can use the `pyproject.toml` file  to set up a virtual environment. This ensures all Python dependencies and the scripts in `src\py-scripts` are installed in the environment. 

To set up a Poetry virtual environment, follow these steps:

```bash
# Navigate to your project directory where your pyproject.toml is located
cd /path/to/your/project

# Install the project dependencies
poetry install

# Activate the virtual environment
poetry shell
```


```bash
# Create a virtual environment
python3 -m venv .venv
# Activate the virtual environment
source .venv/bin/activate
# Install the requirements
pip install -r requirements.txt
```


### Docker

The project root contains a Dockerfile that utilizes a GDAL image and automatically installs dependencies from `pyproject.toml`. This Dockerfile also configures a Jupyter server, enabling the execution of notebooks within the server environment.

#### Build the Docker image

    ```bash
    docker build -t gdal-python:0.0.1 .
    ```

#### Run the Docker image

There are several methods to interact with and run the code within the container. You can utilize Visual Studio Code or a Jupyter server for an interactive approach, or execute scripts directly via the command line.

**Please note**, the container does not include any data. Ensure to mount your data into the container accordingly.

#### 1. Execute in a Container via Visual Studio Code

- Add the volumes to the VS Code docker configuration file `devcontainer.json`. See the template [here](/.devcontainer/template_devcontainer.json).

- Open the command palette and select "Remote-Containers: Reopen in Container"

- Exit the container by clicking the "Remote-Containers: Reopen Locally" button in the bottom right corner of the window.

#### 2. Launch a Jupyter Notebook via Docker Compose

- Run the container with docker-compose: `docker-compose up`
- The `docker-compose.yml` file is configured to mount the `data/` and `config/` directories to the container.
- The Jupyter notebook server is available at `http://localhost:8888`
- The authentication token is printed in the terminal when the server starts `http://localhost:8888/tree?token=...`
- Exit the server by pressing `Ctrl+C` in the terminal and then running `docker-compose down`     

#### 3. Run Scripts or Notebooks from the Command Line

```bash
# $PWD is the current working directory
docker run -it --rm -v $(pwd)/data:/data -v $(pwd)/src:/src gdal-python:0.0.1 /bin/bash

# ls / to see the mounted volumes
ls /data
ls /src

# Run the script
cd /src/shell
./gdal_filegdb-gpkg.sh

# Exit the container
exit
```

## Scripts and Notebooks

More information about the standalone scripts and Jupyter notebooks can be found in the [src/README](/src/README.md) file and the [notebooks/README](/notebooks/README.md) file.

For each project a new notebook is created in the `notebooks/` directory. The notebooks are designed to be run in a Jupyter environment and they utilize the scripts in the `src/` directory. 

**Note**: If you run the notebooks in Colab, you will need to upload the `/data` and `/src` directories to the Colab environment.

```python
# upload the src/ directory to the Colab environment
from google.colab import files
uploaded = files.upload()

# unzip the file
!unzip src.zip
!ls src
```










