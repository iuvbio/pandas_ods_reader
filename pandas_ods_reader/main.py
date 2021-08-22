"""Imports an ods or fods file into a DataFrame object"""
from pathlib import Path

from .parsers import fods, ods
from . import algo


EXT_MAP = {".ods": ods, ".fods": fods}


def read_ods(file_or_path, sheet=1, headers=True, columns=None):
    """
    Read in the provided ods file and convert it to `pandas.DataFrame`.

    Parameters
    ----------
    file_or_path : str
        The path to the .ods or .fods file.
    sheet : int or str, default 1
        If `int`, the 1 based index of the sheet to be read. If `str`, the
        name of the sheet to be read.
    header : bool, default True
        If `True`, then the first row is treated as the list of column names.
    columns : list or None, optional
        A list of column names to be used as headers.

    Returns
    -------
    pandas.DataFrame
        The content of the specified sheet as a DataFrame.
    """
    backend = EXT_MAP.get(Path(file_or_path).suffix)
    if not backend:
        raise ValueError("Unknown filetype.")
    return algo.read_data(
        backend, file_or_path, sheet, headers=headers, columns=columns
    )
