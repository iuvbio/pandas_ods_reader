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
    for i in df.index.tolist()[-1::-1]:
        if df.iloc[i].isna().all():
            df.drop(i, inplace=True)
        else:
            break
    # Delete empty columns
    cols = []
    for column in df:
        if not df[column].isnull().all():
            cols.append(column)
    df = df[cols]
    return df
