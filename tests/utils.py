import logging
import os

LOGGER = logging.getLogger(__name__)


def get_test_file_path(filename: str) -> str:
    """helper function to open test file safely

    Parameters
    ----------
    filename :
        str:
    filename: str :


    Returns
    -------

    """

    # Code copied from pygeoapi
    # https://github.com/geopython/pygeoapi/blob/master/tests/util.py

    if os.path.isfile(filename):
        return filename
    else:
        return f"tests/{filename}"
