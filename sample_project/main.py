"""
Main Script

This script servers as the entry point
for the sub-packages and modules of the project.
"""
import logging
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

import src.decorators as dec  # noqa

# setup logging
from src.logger import setup_logging  # noqa

config_file = os.path.join(project_root, "config/logging.yaml")
setup_logger = setup_logging(config_file)
logger = logging.getLogger(__name__)


def main():
    """example main function"""
    import time

    # log project configuration
    logger.info("Starting main script..")

    @dec.timer
    @dec.dec_logger
    def divide(x, y):
        time.sleep(5)
        result = x / y
        return result

    divide(8, 4)
    divide(10, 0)


if __name__ == "__main__":
    main()
