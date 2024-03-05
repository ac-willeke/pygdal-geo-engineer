
# Use the official GDAL image as the base image
FROM osgeo/gdal:ubuntu-small-3.6.3

# Set the working directory in the container
WORKDIR /app

# Install pip and poetry, and clean up the apt cache
RUN apt-get update && apt-get -y install python3-pip --fix-missing && \
    pip3 install poetry && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# POETRY ==================================================================== #
# copy .toml and .lock files
# set virtualenvs.create to false
# gdal image already comes with a virtualenv
# --no root prevents poetry from using root privileges
# Poetry can only install depedenies in the current .venv

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-root

ENV PATH="/app/venv/bin:$PATH"
# =========================================================================== #

# JUPYTER =================================================================== #
# Create a new user "jupyteruser" and change the owner of /app to jupyteruser
RUN useradd -m jupyteruser && \
    chown jupyteruser:jupyteruser /app

# Expose port 8888 for the Jupyter notebook server
EXPOSE 8888

# Run Jupyter notebook server on container startup
CMD sh -c "hostname -I && jupyter notebook --ip=0.0.0.0 --no-browser"
# =========================================================================== #