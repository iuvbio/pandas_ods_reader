"""Imports an ods or fods file into a DataFrame object"""
from pathlib import Path

from .parsers import fods, ods


EXT_MAP = {".ods": ods, ".fods": fods}


def read_ods(file_or_path, sheet=1, headers=True, columns=None):
    loader = EXT_MAP.get(Path(file_or_path).suffix)
    if not loader:
        raise ValueError("Unknown filetype.")
    return loader.read(file_or_path, sheet, headers=headers, columns=columns)
