import sys

from .main import read_ods


__distname__ = "pandas-ods-reader"

if sys.version_info >= (3, 8):
    import importlib.metadata

    __version__ = importlib.metadata.version(__distname__)
else:
    import pkg_resources

    __version__ = pkg_resources.get_distribution(__distname__).version
