from collections import defaultdict

from lxml import etree
import pandas as pd

from ..tools import sanitize_df


BODY_TAG = "office:body"
SPREADSHEET_TAG = "office:spreadsheet"
OFFICE_KEY = "office"
TABLE_KEY = "table"
TABLE_TAG = "table:table"
TABLE_ROW_TAG = "table:table-row"
TABLE_CELL_TAG = "table:table-cell"
TABLE_CELL_TEXT_TAG = "text:p"
TABLE_CELL_REPEATED_ATTRIB = "number-columns-repeated"
VALUE_TYPE_ATTRIB = "value-type"


def get_sheet(spreadsheet, sheet_id):
    namespaces = spreadsheet.nsmap
    if isinstance(sheet_id, str):
        sheet = spreadsheet.find(
            f"{TABLE_TAG}[@table:name='{sheet_id}']", namespaces=namespaces
        )
        if sheet is None:
            raise KeyError(f"There is no sheet named {sheet_id}.")
        return sheet
    tables = spreadsheet.findall(TABLE_TAG, namespaces=namespaces)
    if sheet_id == 0 or sheet_id > len(tables):
        raise IndexError(f"There is no sheet at index {sheet_id}.")
    return tables[sheet_id - 1]


def parse_columns(cells, headers=True, columns=None):
    orig_columns = cells.pop(0) if headers else None
    if columns is None:
        if orig_columns:
            repeated_val = None
            columns = []
            repeated_dict = defaultdict(lambda: 0)
            for i, col in enumerate(orig_columns):
                text = col.find(TABLE_CELL_TEXT_TAG, namespaces=col.nsmap)
                if text is not None:
                    value = text.text
                elif text is None and repeated_val:
                    value = repeated_val
                else:
                    value = "unnamed"
                    idx = 1
                    while "{}.{}".format(value, idx) in columns:
                        idx += 1
                    value = f"{value}.{idx}"
                repeated = col.attrib.get(
                    f"{{{col.nsmap[TABLE_KEY]}}}{TABLE_CELL_REPEATED_ATTRIB}"
                )
                if repeated:
                    repeated_dict[value] += 1
                    repeated_val = f"{value}.{repeated_dict[value]}"
                column = value if value not in columns else f"{value}.{i}"
                columns.append(column)
        else:
            columns = [f"column.{i}" for i in range(len(cells[0]))]
    return columns, cells


def parse_value(cell):
    text = cell.find(TABLE_CELL_TEXT_TAG, namespaces=cell.nsmap)
    is_float = (
        cell.attrib.get(f"{{{cell.nsmap[OFFICE_KEY]}}}{VALUE_TYPE_ATTRIB}") == "float"
    )
    if text is None:
        return None
    value = text.text
    if is_float:
        return float(value)
    return value


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
    allcells = []
    for row in rows:
        cells = row.findall(TABLE_CELL_TAG, namespaces=namespaces)
        allcells.append(cells)
    columns, values = parse_columns(allcells, headers, columns)
    data = []
    for row in values:
        rowvalues = [parse_value(cell) for cell in row]
        data.append(rowvalues)
    final_rows = []
    for row in data:
        final_row = []
        for i in range(len(columns)):
            if i < len(row):
                final_row.append(row[i])
            else:
                final_row.append(None)
        final_rows.append(final_row)
    return pd.DataFrame(final_rows, columns=columns)


def read(file_or_path, sheet=1, headers=True, columns=None):
    doc = etree.parse(str(file_or_path))
    df = load_fods(doc, sheet, headers=headers, columns=columns)
    return sanitize_df(df)
