"""Provides utility functions for the parser"""


def ods_info(doc):
    """Prints the number of sheets, their names, and number of rows and columns"""
    print("Spreadsheet contains %d sheet(s)." % len(doc.sheets))
    for sheet in doc.sheets:
        print("-"*40)
        print("   Sheet name : '%s'" % sheet.name)
        print("Size of Sheet : (rows=%d, cols=%d)" % (
            sheet.nrows(), sheet.ncols()))


def sanitize_df(df):
    """Drops empty rows and columns from the DataFrame and returns it"""
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
