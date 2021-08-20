import pkg_resources

from .parser import read_ods


__version__ = pkg_resources.get_distribution("pandas_ods_reader").version
