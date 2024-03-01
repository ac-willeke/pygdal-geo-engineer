"""
py-linux-template
=================

A template packagee for Python projects on Linux.
"""

__author__ = "Willeke A'Campo"
__email__ = "willeke.acampo@nina.no"
__version__ = "0.1.0"

import logging

# local imports
from src.logger import setup_logging  # noqa
from src.utils import yaml_load  # noqa

logging.getLogger(__name__).addHandler(logging.NullHandler())
