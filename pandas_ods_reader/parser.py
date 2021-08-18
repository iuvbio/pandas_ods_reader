"""Imports an ods file into a DataFrame object"""
import ezodf

from .parsers import ods
from .tools import sanitize_df


def read_ods(file_or_path, sheet=1, headers=True, columns=None):
    """
    This function reads in the provided ods file and converts it to a
    dictionary. The dictionary is converted to a DataFrame. Trailing empty rows
    and columns are dropped from the DataFrame, before it is returned.

    :param file_or_path: str
    the path to the ODS file
    :param sheet: int or str, default 1
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
    df = ods.load_ods(doc, sheet, headers, columns)
    return sanitize_df(df)
