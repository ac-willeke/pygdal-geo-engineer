import datetime
import logging
import logging.config
import os
import sys

import yaml

from py_scripts import PROJECT_ROOT
config_file = os.path.join(PROJECT_ROOT, "config/logging.yaml")


def reset_logger():
    """Reset the logger configuration to default."""
    logging.shutdown()
    logging.root.handlers = []  # Remove all handlers
    logging.root.setLevel(logging.WARNING)  # Set the root logger to a default level
    return


def setup_logging(
    path= os.path.join(PROJECT_ROOT, "config/logging.yaml"),
    default_level=logging.INFO,
    default_name=None
):
    """
    Setup logging configuration

    Parameters
    ----------
    path : str
        Default value = 'config/logging.yaml')
    default_level : logging level
        Default value = logging.INFO)

    Returns
    -------
    Void
        Creates logging instance
    """

    if os.path.exists(path):
        with open(path, "rt") as f:
            config = yaml.safe_load(f.read())

        # if default_name is provided: time_stamp_default_name.log
        if default_name:
            logfile_name = (
                datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                + "_"
                + default_name
                + ".log"
            )
        else:
            # generate logfile_name
            logfile_name = (
                datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                + "_"
                + os.path.splitext(os.path.basename(sys.argv[0]))[0]
                + ".log"
            )

        # Check if log directory exists for info log file
        info_log_file_path = os.path.join(PROJECT_ROOT, "log", logfile_name)

        # Check if the log directory exists, create if not
        info_log_dir = os.path.dirname(info_log_file_path)
        if not os.path.exists(info_log_dir):
            os.makedirs(info_log_dir, exist_ok=True)
            
        # Update info file handler with the new log file path
        config["handlers"]["info_file_handler"]["filename"] = info_log_file_path

        # For error log file, repeat the process
        # Assuming you want a separate error log file, modify the name accordingly
        error_logfile_name = "error_" + logfile_name
        error_log_file_path = os.path.join(PROJECT_ROOT, "log", error_logfile_name)

        # Check if the log directory exists for error log file, create if not
        error_log_dir = os.path.dirname(error_log_file_path)
        if not os.path.exists(error_log_dir):
            os.makedirs(error_log_dir, exist_ok=True)

        # Update error file handler with the new log file path
        config["handlers"]["error_file_handler"]["filename"] = error_log_file_path

        # load configuration
        logging.config.dictConfig(config)
        logging.info("Logging configuration file found and loaded.")

    else:
        logging.basicConfig(level=default_level)
        logging.info(
            "Logging configuration file not found. Using default configuration."
        )


## Example usage of logger within modules
## TODO move to tests/test_logger.py
def test_function():
    """Test function for logging"""

    logger = logging.getLogger(__name__)
    logger.info("This is a information message.")
    logger.debug("This is a debug message.")
    logger.warning("This is a warning message.")
    logger.error("This is a error message.")
    logger.critical("This is a critical message.")
    return


class Test(object):
    """
    Test class for logging.

    Parameters
    ----------
    logger : logging instance
        Default value = None

    Attributes
    ----------
    logger : logging instance
        Default value = None

    Methods
    -------
        - log_config: Log project configuration
        - log_best_practices: Log best practices
    """

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def log_config(self):
        """Log project configuration"""
        try:
            # loaded as module
            from py_scripts.config import load_catalog, load_parameters  # noqa
        except ModuleNotFoundError:
            # standalone use of logger.py
            from config import load_catalog, load_parameters  # noqa

        self.logger.info("Project configuration:")

        catalog = load_catalog()
        parameters = load_parameters()
        # Access configuration variables
        self.logger.info("DATA: %s", catalog["project_data"]["filepath"])
        self.logger.info(
            "SPATIAL_REFERENCE: %s", parameters["spatial_reference"]["utm33"]
        )

    def log_best_practices(self):
        """Log best practices"""
        self.logger.info("Logging best practices:")
        self.logger.info("Use __name__ as the logger name.")
        self.logger.info(
            "Do not use logger at module level,\n\
            get logger within functions or classes instead.\n\
            Otherwise, the logger will be initialized when the module is imported,\n\
            this is often before the logging configuration is set up."
        )

if __name__ == "__main__":
    # setup loggging for standalone use of logger.py
    setup_logging()

    # test project logger
    Test().log_config()
    Test().log_best_practices()

    # test custom logger
    test_function()

    pass
