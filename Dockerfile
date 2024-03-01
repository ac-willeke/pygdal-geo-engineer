
# Use the official GDAL image as the base image
FROM osgeo/gdal:ubuntu-small-3.6.3

# install pip
RUN apt-get update && apt-get -y install python3-pip --fix-missing

# install poetry
RUN pip3 install poetry

# Set the working directory in the container
WORKDIR /app

# --- Install all poetry dependencies ---
# copy .toml and .lock files)
# set virtualenvs.create to false, gdal image already comes with a virtualenv
# --no root prevents poetry from using root privileges.
# Poetry is only able to install depedences in the current venv.
# More secure and isolated
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
# ---------------------------------------

# Change path to poetry venv
RUN export PATH="/app/venv/bin:$PATH"

#EXPOSE 8888
#CMD ["jupyter", "notebook", "--"]
