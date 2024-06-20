""" Decorators for the project. """

# NOTE:
# *args allow our function to take any number of positional arguments (stored in a tuple)
# ** kwargs allow our function to take any number of keyword arguments (stored in a dictionary)
import logging
from functools import wraps


def timer(func):
    """
    A decorator that times a function.

    Parameters
    ----------
    func : function
        Function to be timed.

    Returns
    -------
    type
        Function output.

    """

    import time

    logger = logging.getLogger(__name__)

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        # call the function
        output = func(*args, **kwargs)
        end = time.perf_counter()
        logger.info(f"Execution time {func.__name__}(): {end - start:.2f} sec")
        return output

    return wrapper


# decorater that catches exceptions
def exception_handler(func):
    """A decorator that catches exceptions."""

    logger = logging.getLogger(__name__)

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            output = func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Exception in [{func.__name__}]: {e}")
            output = None
        return output

    return wrapper


def dec_logger(func):
    """A decorator that logs a function with info and error messages."""
    
    logger = logging.getLogger(__name__)

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"------ start function: {func.__name__} ------")
        try:
            logger.info(f"Run with args: {args}, and kwargs: {kwargs}")
            output = func(*args, **kwargs)
            logger.info(f"Returned: - End function {output!r}")
        except Exception as e:
            logger.error(f"Raised Exception in {func.__name__}(): {e}")
            output = None
            logger.info(f"Returned: - End function {output!r}")

        return output

    return wrapper


def main():
    # simple console logger
    import time

    logger = logging.getLogger(__name__)

    @timer
    @dec_logger
    def test_timer():
        """Test function for timer decorator."""
        logger.info("Testing timer decorator...")
        time.sleep(5)
        return

    @timer  # track total execution time, including exception handling + logger
    @exception_handler
    @dec_logger
    def divide(x, y):
        result = x / y
        return result

    test_timer()
    divide(10, 0)


if __name__ == "__main__":

    # set up logging
    from py_scripts.logger import setup_logging
    setup_logging()
    
    # test decorators
    main()
