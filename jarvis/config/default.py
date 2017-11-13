"""Config options available for the Jarvis setup."""

from oslo_config import cfg

from jarvis.config import base as conf_base


class JarvisOptions(conf_base.Options):

    """Config options available for the Jarvis setup."""

    def __init__(self, config):
        super(JarvisOptions, self).__init__(config, group="DEFAULT")
        self._options = []

    def register(self):
        """Register the current options to the global ConfigOpts object."""
        group = cfg.OptGroup(self.group_name, title='Jarvis Options')
        self._config.register_group(group)
        self._config.register_opts(self._options, group=group)

    def list(self):
        """Return a list which contains all the available options."""
        return self._options
