import logging
import os
from flaskr.lib import settings


def create_logger():
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(settings.log_level)

    # create the logging file handler
    fh = logging.FileHandler(os.getcwd() + "/logs/dummy.log")

    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)

    # add handler to logger object
    logger.addHandler(fh)
    return logger
