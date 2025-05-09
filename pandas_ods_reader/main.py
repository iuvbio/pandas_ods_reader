"""Imports an ods or fods file into a DataFrame object"""

from pathlib import Path
from typing import Optional, List, Union

import pandas as pd

from .parsers import fods, ods
from . import algo


EXT_MAP = {".ods": ods, ".fods": fods}


def read_ods(
    file_or_path: Union[str, Path],
    sheet: Union[str, int] = 1,
    headers: bool = True,
    columns: Optional[List[str]] = None,
    skiprows: int = 0,
) -> pd.DataFrame:
    """
    Read in the provided ods or .ods file and convert it to `pandas.DataFrame`.
    Will detect the filetype based on the file's extension or fall back to
    ods.

    Args:
        file_or_path: The path to the .ods or .fods file.
        sheet: If `int`, the 1 based index of the sheet to be read. If `str`, the
            name of the sheet to be read.
        headers: If `True`, then the first row is treated as the list of column names.
        columns: A list of column names to be used as headers.
        skiprows: The number of rows to skip before starting to read data.

    Returns:
        The content of the specified sheet as a DataFrame.
    """
    path = file_or_path if isinstance(file_or_path, Path) else Path(file_or_path)
    if not path.is_file():
        raise FileNotFoundError(f"file {path} does not exist")
    backend = EXT_MAP.get(path.suffix, ods)
    return algo.read_data(
        backend,
        path,
        sheet,
        headers=headers,
        columns=columns or [],
        skiprows=skiprows,
    )
