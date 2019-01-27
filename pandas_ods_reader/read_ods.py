"""Imports an ods file into a DataFrame object"""
import ezodf
import pandas as pd


def ods_info(doc):
    print("Spreadsheet contains %d sheet(s)." % len(doc.sheets))
    for sheet in doc.sheets:
        print("-"*40)
        print("   Sheet name : '%s'" % sheet.name)
        print("Size of Sheet : (rows=%d, cols=%d)" % (
            sheet.nrows(), sheet.ncols()))


def load_ods(doc, sheet, headers=True, columns=None):
    # convert the sheet to a pandas.DataFrame
    if isinstance(sheet, int):
        sheet = doc.sheets[sheet - 1]
    elif isinstance(sheet, str):
        sheets = [sheet.name for sheet in doc.sheets]
        if sheet not in sheets:
            raise ValueError("There is no sheet named {}".format(sheet))
        sheet_idx = sheets.index(sheet)
        sheet = doc.sheets[sheet_idx]
    df_dict = {}
    col_index = {}
    for i, row in enumerate(sheet.rows()):
        # row is a list of cells
        if headers and i == 0:
            # columns as lists in a dictionary
            df_dict = {cell.value: [] for cell in row if cell.value}
            # create index for the column headers
            col_index = {
                j: cell.value for j, cell in enumerate(row) if cell.value}
            continue
        elif not headers and i == 0:
            columns = columns if columns else (
                ["Column_%s" % j for j in range(len(row))])
            # columns as lists in a dictionary
            df_dict = {column: [] for column in columns}
            # create index for the column headers
            col_index = {j: column for j, column in enumerate(columns)}
            continue
        for j, cell in enumerate(row):
            if j < len(col_index):
                # use header instead of column index
                df_dict[col_index[j]].append(cell.value)
            else:
                continue
    # and convert to a DataFrame
    df = pd.DataFrame(df_dict)
    return df


def sanitize_df(df):
    # Delete empty rows
    rows = len(df) - 1
    for i in range(rows):
        row = df.iloc[-1]
        if row.isnull().all():
            df = df.iloc[:-2]
        else:
            break
    # Delete empty columns
    cols = []
    for column in df:
        if not df[column].isnull().all():
            cols.append(column)
    df = df[cols]
    len(df.columns)
    return df


def read_ods(file_or_path, sheet, headers=True, columns=None):
    """
    This function reads in the provided ods file and converts it to a
    dictionary. The dictionary is converted to a DataFrame. Empty rows and
    columns are dropped from the DataFrame, before it is returned.

    :param file_or_path: str
    the path to the ODS file
    :param sheet: int or str
    if int, the 1 based index of the sheet to be read in. If str, the name of
    the sheet to be read in
    :param header: bool, default True
    if True, the first row is read in as headers
    :param columns: list, default None
    a list of column names to be used as headers
    :returns: pandas.DataFrame
    the ODS file as a pandas DataFrame
    """
    doc = ezodf.opendoc(file_or_path)
    df = load_ods(doc, sheet, headers, columns)
    return sanitize_df(df)
