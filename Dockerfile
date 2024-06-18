
# base image: gdal
# ensure py-gdal bindings installed with poetry are similar to gdal image
FROM osgeo/gdal:ubuntu-small-3.6.3

# Set the wd
WORKDIR /app

# Install dependencies in one layer to optimize build cache
RUN apt-get update && \
    apt-get -y install python3-pip --fix-missing && \
    pip3 install poetry && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Add src to PYTHONPATH
COPY . /app/
# Set the PYTHONPATH environment variable
ENV PYTHONPATH="/workspaces/pygdal-geo-engineer/src:/app/src:${PYTHONPATH}"

# POETRY ==================================================================== #
# install poetry dependencies in base python
COPY pyproject.toml /app/

RUN poetry config virtualenvs.create false && \
    poetry install --no-root

ENV PATH="/app/venv/bin:$PATH"
# =========================================================================== #

# JUPYTER =================================================================== #
# Create a new user "jupyteruser" and change the owner of /app to jupyteruser
RUN useradd -m jupyteruser && \
    chown jupyteruser:jupyteruser /app

#USER jupyteruser

# Expose port 8888 for the Jupyter notebook server
EXPOSE 8888

# Run Jupyter notebook server on container startup
CMD sh -c "hostname -I && jupyter notebook --ip=0.0.0.0 --no-browser"
# =========================================================================== #