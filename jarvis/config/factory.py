"""Config options factory."""

_OPT_PATHS = (
    'jarvis.config.default.JarvisOptions',
)


def _load_class(class_path):
    """Load the module and return the required class."""
    parts = class_path.rsplit('.', 1)
    module = __import__(parts[0], fromlist=parts[1])
    return getattr(module, parts[1])


def get_options():
    """Return a list of all the available `Options` subclasses."""
    return [_load_class(class_path) for class_path in _OPT_PATHS]
