"""The module contains the / endpoint object for Jarvis API."""

import os

import cherrypy

from jarvis.api import base as api_base
from jarvis.api import v1 as api_v1
from jarvis import config as jarvis_config

CONFIG = jarvis_config.CONFIG


class Root(api_base.BaseAPI):

    """The / endpoint for the Jarvis API."""

    resources = [
        ("v1", api_v1.JarvisV1),
    ]

    @classmethod
    def config(cls):
        """Prepare the configurations for the current metadata service."""
        return {
            'global': {
                'server.socket_host': CONFIG.api.host,
                'server.socket_port': CONFIG.api.port,
                'environment': CONFIG.api.environment,
                'log.screen': False,
                'log.error_file': os.path.join(CONFIG.log_dir or "",
                                               "jarvis-api-error.log"),
                'server.thread_pool': CONFIG.api.thread_pool,
            },
            '/': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher()
            }
        }
