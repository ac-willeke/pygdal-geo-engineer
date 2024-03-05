PYGDAL-GEO-ENGINEER
==============================

**repo-status: work in progress**

A collection of scripts to perform geospatial engineering tasks using GDAL, Python and SQL. The scripts are organized in a modular way under `src/` and are designed to be run from the command line or within a Jupyter notebook.

## Installation 

1. Clone the repository and navigate to the project directory

2. Build the docker image

    ```bash
    docker build -t gdal-python:0.0.1 .
    ```

## Usage

#### Run in **Visual Studio Code**

- Add the volumes to the VS Code docker configuration file `devcontainer.json`. See the template [here](/.devcontainer/template_devcontainer.json).

- Open the command palette and select "Remote-Containers: Reopen in Container"

#### Run a script or notebook from the command line

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

#### Run a Jupyter notebook by starting the Jupyter server using Docker Compose

- Run the container with docker-compose: `docker-compose up`
- The `docker-compose.yml` file is configured to mount the `data/` and `config/` directories to the container.
- The Jupyter notebook server is available at `http://localhost:8888`
- The authentication token is printed in the terminal when the server starts `http://localhost:8888/tree?token=...`
    
     
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










