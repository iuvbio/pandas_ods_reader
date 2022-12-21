from .main import read_ods

from importlib.metadata import version

__version__ = version("pandas-ods-reader")

__all__ = ("read_ods", "__version__")
