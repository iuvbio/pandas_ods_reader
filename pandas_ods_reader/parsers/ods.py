from pathlib import Path
from typing import Any, Iterator, Union

import ezodf
from ezodf.document import FlatXMLDocument, PackagedDocument


def get_doc(file_or_path: Path) -> Union[FlatXMLDocument, PackagedDocument]:
    return ezodf.opendoc(file_or_path)


def get_rows(
    doc: Union[FlatXMLDocument, PackagedDocument],
    sheet_id: Union[str, int],
) -> Iterator[list[ezodf.Cell]]:
    if not isinstance(sheet_id, (int, str)):
        raise ValueError("Sheet id has to be either `str` or `int`")
    if isinstance(sheet_id, str):
        sheets: list[str] = [sheet.name for sheet in doc.sheets]
        if sheet_id not in sheets:
            raise KeyError("There is no sheet named {}".format(sheet_id))
        sheet_id = sheets.index(sheet_id) + 1
    sheet: ezodf.Sheet = doc.sheets[sheet_id - 1]
    return sheet.rows()


def get_value(cell: ezodf.Cell, parsed: bool = False) -> tuple[Any, int]:
    return cell.value, 0
