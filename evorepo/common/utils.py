"""Utilities and helper functions."""
import sys
import logging

from evorepo import config as global_config


def get_logger(name=None, format_string=None):
    """Obtain a new logger object.

    :param name:          the name of the logger
    :param format_string: the format it will use for logging.

    If it is not given, the the one given at command
    line will be used, otherwise the default format.
    """
    name = name or global_config.log["name"]
    format_string = format_string or global_config.log["format"]
    logger = logging.getLogger(name)
    formatter = logging.Formatter(format_string)

    if not logger.handlers:
        # If the logger wasn't obtained another time,
        # then it shouldn't have any loggers

        if global_config.log["file"]:
            file_handler = logging.FileHandler(global_config.log["file"])
            file_handler.setFormatter(formatter)
            file_handler.setLevel(global_config.log["file_level"])
            logger.addHandler(file_handler)

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        stdout_handler.setLevel(global_config.log["cli_level"])
        logger.addHandler(stdout_handler)

    return logger
