"""Project configuration"""

import os
import logging
from pathlib import Path

from py_scripts.utils import yaml_load
from py_scripts.logger import setup_logging, Test 
from py_scripts import PROJECT_ROOT

# --------------------------------------------------------------------------- #
# Load secure variables from .env file
# --------------------------------------------------------------------------- #

# for .env file in USER directory
# user_dir = C:\\USERS\\<<firstname.lastname>>
# user_dir = os.path.join(os.path.expanduser("~"))
# dotenv_path = os.path.join(user_dir, ".env")
# print(dotenv_path)
# load_dotenv(dotenv_path)


# --------------------------------------------------------------------------- #
def load_catalog():
    catalog = os.path.join(PROJECT_ROOT, "config/catalog.yaml")
    with open(catalog, "r") as f:
        catalog = yaml_load(f)

    return catalog


def load_parameters():
    parameters = os.path.join(PROJECT_ROOT, "config/parameters.yaml")
    with open(parameters, "r") as f:
        parameters = yaml_load(f)
    return parameters


# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # set up logging
    setup_logging()
    logger = logging.getLogger(__name__)
 
    # load catalog
    logger.info("Loading catalog...")
    catalog = load_catalog()
    parameters = load_parameters()
    logger.info(catalog["project_data"]["filepath"])
