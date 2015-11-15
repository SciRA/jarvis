"""Shared constants across the Jarvis project."""
import logging


ENVIRONMENT = {
    "development": {
        "log.name": "jarvis-dev",
        "log.cli_level": logging.DEBUG,
        "log.file_level": logging.DEBUG,
        "log.format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "log.file": None,
        "misc.attempts": 3,
        "misc.retry_interval": 0.1,
    },
    "production": {
        "log.name": "jarvis",
        "log.cli_level": logging.INFO,
        "log.file_level": logging.INFO,
        "log.format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "log.file": None,
        "misc.attempts": 5,
        "misc.retry_interval": 0.2,
    }
}
