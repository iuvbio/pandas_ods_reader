from collections import OrderedDict

import pandas as pd

from .utils import sanitize_df


def parse_data(backend, rows, headers=True, columns=None):
    df_dict = OrderedDict()
    col_index = {}
    for i, row in enumerate(rows):
        # row is a list of cells
        if headers and i == 0 and not columns:
            repeat_until = -1
            repeat_value = None
            # columns as lists in a dictionary
            columns = []
            # parse the first row as column names
            for k, cell in enumerate(row):
                value, n_repeated = backend.get_value(cell)
                if n_repeated > 0:
                    repeat_value = value
                    repeat_until = n_repeated + k
                if not value and k <= repeat_until:
                    value = repeat_value
                if k == repeat_until:
                    # reset to allow for more than one repeated column
                    repeat_until = -1
                if value and value not in columns:
                    columns.append(value)
                else:
                    column_name = value if value else "unnamed"
                    # add count to column name
                    idx = 1
                    while f"{column_name}.{idx}" in columns:
                        idx += 1
                    columns.append(f"{column_name}.{idx}")
        elif i == 0:
            # without headers, assign generic numbered column names
            columns = columns if columns else [f"column.{j}" for j in range(len(row))]
        if i == 0:
            df_dict = OrderedDict((column, []) for column in columns)
            # create index for the column headers
            col_index = {j: column for j, column in enumerate(columns)}
            if headers:
                continue
        for j, cell in enumerate(row):
            if j < len(col_index):
                value, _ = backend.get_value(cell, parsed=True)
                # use header instead of column index
                df_dict[col_index[j]].append(value)
    # make sure all columns are of the same length
    max_col_length = max(len(df_dict[col]) for col in df_dict)
    for col in df_dict:
        col_length = len(df_dict[col])
        if col_length < max_col_length:
            df_dict[col] += [None] * (max_col_length - col_length)
    df = pd.DataFrame(df_dict)
    return df


def read_data(backend, file_or_path, sheet_id, headers=True, columns=None):
    doc = backend.get_doc(file_or_path)
    rows = backend.get_rows(doc, sheet_id)
    df = parse_data(backend, rows, headers=headers, columns=columns)
    return sanitize_df(df)
