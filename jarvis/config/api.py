"""Config options available for the Jarvis setup."""

from oslo_config import cfg

from jarvis.config import base as conf_base


class JarvisAPIOptions(conf_base.Options):

    """Config options available for the jarvis setup."""

    def __init__(self, config):
        super(JarvisAPIOptions, self).__init__(config, group="api")
        self._options = [
            cfg.StrOpt(
                "host", default="0.0.0.0",
                help="The IP address or the host name of the server."),
            cfg.IntOpt(
                "port", default=8080, required=True,
                help="The port that should be used by the current "
                     "metadata service."),
            cfg.StrOpt(
                "environment", default="production", required=True,
                help="Apply the given config environment."),
            cfg.IntOpt(
                "thread_pool", default=3, required=True,
                help="The number of thread workers used in order "
                     "to serve clients."),
        ]

    def register(self):
        """Register the current options to the global ConfigOpts object."""
        group = cfg.OptGroup(self.group_name, title='Jarvis API Options')
        self._config.register_group(group)
        self._config.register_opts(self._options, group=group)

    def list(self):
        """Return a list which contains all the available options."""
        return self._options
