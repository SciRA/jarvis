"""The entry point for the oslo configuration generator."""

import collections

from jarvis.config import base as conf_base
from jarvis.config import factory as conf_factory


def get_options():
    """Collect all the options info from the other modules."""
    options = collections.defaultdict(list)
    for opt_class in conf_factory.get_options():
        if not issubclass(opt_class, conf_base.Options):
            continue
        config_options = opt_class(None)
        options[config_options.group_name].extend(config_options.list())
    return [(key, value) for key, value in options.items()]
