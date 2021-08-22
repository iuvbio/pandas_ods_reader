import ezodf


def get_doc(file_or_path):
    return ezodf.opendoc(file_or_path)


def get_rows(doc, sheet_id):
    if not isinstance(sheet_id, (int, str)):
        raise ValueError("Sheet id has to be either `str` or `int`")
    if isinstance(sheet_id, str):
        sheets = [sheet.name for sheet in doc.sheets]
        if sheet_id not in sheets:
            raise KeyError("There is no sheet named {}".format(sheet_id))
        sheet_id = sheets.index(sheet_id) + 1
    sheet = doc.sheets[sheet_id - 1]
    return sheet.rows()


def get_value(cell, parsed=False):
    return cell.value, 0
