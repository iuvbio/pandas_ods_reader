from lxml import etree


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


def get_doc(file_or_path):
    return etree.parse(str(file_or_path))


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


def get_rows(doc, sheet_id):
    if not isinstance(sheet_id, (str, int)):
        raise ValueError("Sheet id has to be either `str` or `int`")
    root = doc.getroot()
    namespaces = root.nsmap
    spreadsheet = doc.find(BODY_TAG, namespaces=namespaces).find(
        SPREADSHEET_TAG, namespaces=namespaces
    )
    sheet = get_sheet(spreadsheet, sheet_id)
    rows = sheet.findall(TABLE_ROW_TAG, namespaces=namespaces)
    return rows


def is_float(cell):
    return (
        cell.attrib.get(f"{{{cell.nsmap[OFFICE_KEY]}}}{VALUE_TYPE_ATTRIB}") == "float"
    )


def get_value(cell, parsed=False):
    text = cell.find(TABLE_CELL_TEXT_TAG, namespaces=cell.nsmap)
    if text is None:
        return None, 0
    value = text.text
    if parsed and is_float(cell):
        value = float(value)
    n_repeated = cell.attrib.get(
        f"{{{cell.nsmap[TABLE_KEY]}}}{TABLE_CELL_REPEATED_ATTRIB}"
    )
    n_repeated = int(n_repeated) if n_repeated is not None else 0
    return value, n_repeated
