"""Initialize the Jarvis configurations."""

import os

from oslo_config import cfg
from oslo_log import log as logging

from jarvis.config import factory
from jarvis import version

CONFIG = cfg.ConfigOpts()

logging.register_options(CONFIG)
for option_class in factory.get_options():
    option_class(CONFIG).register()

_DEFAULT_CONFIG_FILES = [
    config_file for config_file in ("/etc/jarvis/jarvis.conf",
                                    "etc/jarvis/jarvis.conf", "jarvis.conf")
    if os.path.isfile(config_file)
]

if _DEFAULT_CONFIG_FILES:
    CONFIG([], project='jarvis', version=version.get_version(),
           default_config_files=_DEFAULT_CONFIG_FILES)
