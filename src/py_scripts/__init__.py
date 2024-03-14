"""
py-scripts
=================

A collection of python scripts for geospatial data processing.
"""

__author__ = "Willeke A'Campo"
__email__ = "willeke.acampo@nina.no"
__version__ = "0.1.0"

import logging
import os
from pathlib import Path

logging.getLogger(__name__).addHandler(logging.NullHandler())

PROJECT_ROOT = Path(__file__).parents[2]
