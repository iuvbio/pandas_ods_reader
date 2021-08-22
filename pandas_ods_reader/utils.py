"""Provides utility functions for the parser"""


def ods_info(doc):
    """Print the number of sheets, their names, and number of rows and columns"""
    print("Spreadsheet contains {:d} sheet(s).".format(len(doc.sheets)))
    for sheet in doc.sheets:
        print("-" * 40)
        print("   Sheet name : '{}'".format(sheet.name))
        print(
            "Size of Sheet : (rows={:d}, cols={:d})".format(
                sheet.nrows(), sheet.ncols()
            )
        )


def sanitize_df(df):
    """Drop empty rows and columns from the DataFrame and returns it"""
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
