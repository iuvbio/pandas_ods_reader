from collections import OrderedDict

import ezodf
import pandas as pd

from ..tools import sanitize_df


def load_ods(doc, sheet_id, headers=True, columns=None):
    # convert the sheet to a pandas.DataFrame
    if not isinstance(sheet_id, (int, str)):
        raise ValueError("Sheet id has to be either `str` or `int`")
    if isinstance(sheet_id, str):
        sheets = [sheet.name for sheet in doc.sheets]
        if sheet_id not in sheets:
            raise KeyError("There is no sheet named {}".format(sheet_id))
        sheet_id = sheets.index(sheet_id) + 1
    sheet = doc.sheets[sheet_id - 1]
    df_dict = OrderedDict()
    col_index = {}
    for i, row in enumerate(sheet.rows()):
        # row is a list of cells
        if headers and i == 0 and not columns:
            # columns as lists in a dictionary
            columns = []
            for cell in row:
                if cell.value and cell.value not in columns:
                    columns.append(cell.value)
                else:
                    column_name = cell.value if cell.value else "unnamed"
                    # add count to column name
                    idx = 1
                    while "{}.{}".format(column_name, idx) in columns:
                        idx += 1
                    columns.append("{}.{}".format(column_name, idx))

            df_dict = OrderedDict((column, []) for column in columns)
            # create index for the column headers
            col_index = {j: column for j, column in enumerate(columns)}
            continue
        elif i == 0:
            columns = columns if columns else ([f"column.{j}" for j in range(len(row))])
            # columns as lists in a dictionary
            df_dict = OrderedDict((column, []) for column in columns)
            # create index for the column headers
            col_index = {j: column for j, column in enumerate(columns)}
            if headers:
                continue
        for j, cell in enumerate(row):
            if j < len(col_index):
                # use header instead of column index
                df_dict[col_index[j]].append(cell.value)
            else:
                continue
    df = pd.DataFrame(df_dict)
    return df


def read(file_or_path, sheet=1, headers=True, columns=None):
    doc = ezodf.opendoc(file_or_path)
    df = load_ods(doc, sheet, headers, columns)
    return sanitize_df(df)
