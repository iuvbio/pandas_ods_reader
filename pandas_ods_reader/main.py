"""Imports an ods or fods file into a DataFrame object"""
from pathlib import Path

from .parsers import fods, ods
from . import algo


EXT_MAP = {".ods": ods, ".fods": fods}


def read_ods(file_or_path, sheet=1, headers=True, columns=None, skiprows=0):
    """
    Read in the provided ods or .ods file and convert it to `pandas.DataFrame`.
    Will detect the filetype based on the file's extension or fall back to
    ods.

    Parameters
    ----------
    file_or_path : str or pathlib.Path
        The path to the .ods or .fods file.
    sheet : int or str, default 1
        If `int`, the 1 based index of the sheet to be read. If `str`, the
        name of the sheet to be read.
    headers : bool, default True
        If `True`, then the first row is treated as the list of column names.
    columns : list, default None, optional
        A list of column names to be used as headers.

    Returns
    -------
    pandas.DataFrame
        The content of the specified sheet as a DataFrame.
    """
    backend = EXT_MAP.get(Path(file_or_path).suffix, ods)
    return algo.read_data(
        backend,
        file_or_path,
        sheet,
        headers=headers, columns=columns, skiprows=skiprows
    )
