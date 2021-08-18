from collections import OrderedDict

from lxml import etree
import pandas as pd


BODY_TAG = "office:body"
SPREADSHEET_TAG = "office:spreadsheet"
TABLE_TAG = "table:table"
TABLE_ROW_TAG = "table:table-row"
TABLE_CELL_TAG = "table:table-cell"
TABLE_CELL_TEXT_TAG = "text:p"


def get_sheet(spreadsheet, sheet_id):
    namespaces = spreadsheet.nsmap
    if isinstance(sheet_id, str):
        sheet = spreadsheet.find(
            f"{TABLE_TAG}[@table:name='{sheet_id}']", namespaces=namespaces
        )
        if sheet is None:
            raise KeyError(f"There is no sheet named {sheet_id}")
        return sheet
    tables = spreadsheet.findall(TABLE_TAG, namespaces=namespaces)
    if sheet_id == 0 or sheet_id > len(tables):
        raise IndexError(f"There is no sheet at index {sheet_id}.")
    return tables[sheet_id - 1]


def load_fods(doc, sheet_id, headers=True, columns=None):
    if not isinstance(sheet_id, (str, int)):
        raise ValueError("Sheet id has to be either `str` or `int`")
    root = doc.getroot()
    namespaces = root.nsmap
    spreadsheet = doc.find(BODY_TAG, namespaces=namespaces).find(
        SPREADSHEET_TAG, namespaces=namespaces
    )
    sheet = get_sheet(spreadsheet, sheet_id)
    rows = sheet.findall(TABLE_ROW_TAG, namespaces=namespaces)
    data = []
    for row in rows:
        cells = row.findall(TABLE_CELL_TAG, namespaces=namespaces)
        data.append(
            [
                cell.find(TABLE_CELL_TEXT_TAG, namespaces=namespaces).text
                for cell in cells
            ]
        )
    orig_columns = data.pop(0) if headers else None
    if columns is None:
        if orig_columns:
            columns = orig_columns
        else:
            columns = [f"column.{i}" for i in range(len(data[0]))]
    return pd.DataFrame(
        OrderedDict({column: datarow for column, datarow in zip(columns, data)})
    )


def read_fods(file_or_path, sheet=1, headers=True, columns=None):
    doc = etree.parse(file_or_path)
    df = load_fods(doc, sheet, headers=headers, columns=columns)
    return df
