"""Shared constants across the Jarvis project."""
import logging


DEFAULTS = {
    "log.verbosity": 0,
    "log.file.level": logging.DEBUG,
    "log.file.format": "%(asctime)s,%(name)s,%(levelname)s,%(message)s",
}

ENVIRONMENT = {
    "development": {
        "log.cli.format": "%(name)s - [%(levelname)s]: %(message)s",
        "log.cli.level": logging.DEBUG,
        "log.file.path": "/tmp/jarvis/jarvis-devel.log",
        "misc.attempts": 3,
        "misc.retry_interval": 0.1,
    },

    "production": {
        "log.cli.format": "[%(levelname)s]: %(message)s",
        "log.cli.level": logging.INFO,
        "log.file.path": "/tmp/jarvis/jarvis.log",
        "misc.attempts": 4,
        "misc.retry_interval": 0.5,
    }
}
