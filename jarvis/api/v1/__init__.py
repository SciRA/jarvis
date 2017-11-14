"""Jarvis API version 1."""

from jarvis.api import base as base_api


class JarvisV1(base_api.BaseAPI):

    """Jarvis API version 1."""

    resources = []
    """A list that contains all the resources (endpoints) available for the
    current metadata service."""

    exposed = True
    """Whether this application should be available for clients."""
