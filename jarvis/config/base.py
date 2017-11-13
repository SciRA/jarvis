"""The contact class for the config options collections."""

import abc

import six


@six.add_metaclass(abc.ABCMeta)
class Options(object):

    """Contract class for all the collections of config options."""

    def __init__(self, config, group="DEFAULT"):
        self._config = config
        self._group_name = group

    @property
    def group_name(self):
        """The group name for the current options."""
        return self._group_name

    @abc.abstractmethod
    def register(self):
        """Register the current options to the global ConfigOpts object."""
        pass

    @abc.abstractmethod
    def list(self):
        """Return a list which contains all the available options."""
        pass
