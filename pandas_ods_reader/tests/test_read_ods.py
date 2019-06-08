import os

import pandas as pd
import pytest

from pandas_ods_reader import read_ods


root = os.path.dirname(os.path.abspath(__file__))
rsc = os.path.join(root, "rsc")

header_file = "example_headers.ods"
no_header_file = "example_no_headers.ods"
duplicated_column_names_file = "example_duplicated_column_names.ods"
col_len_file = "example_col_lengths.ods"
missing_header_file = "example_missing_header.ods"


class TestOdsReader(object):
    def test_header_file_with_int(self):
        path = os.path.join(rsc, header_file)
        df = read_ods(path, 1)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 10
        assert (len(df.columns) == 5)

    def test_header_file_with_str(self):
        path = os.path.join(rsc, header_file)
        df = read_ods(path, "Sheet1")
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 10
        assert (len(df.columns) == 5)

    def test_header_file_with_cols(self):
        path = os.path.join(rsc, header_file)
        columns = ["One", "Two", "Three", "Four", "Five"]
        df = read_ods(path, "Sheet1", columns=columns)
        assert list(df.columns) == columns
        assert len(df) == 10
        assert (len(df.columns) == 5)

    def test_no_header_file_no_cols(self):
        path = os.path.join(rsc, no_header_file)
        df = read_ods(path, 1, headers=False)
        assert list(df.columns) == [
            f"column_{i}" for i in range(len(df.columns))]
        assert len(df) == 10
        assert (len(df.columns) == 5)

    def test_no_header_file_with_cols(self):
        path = os.path.join(rsc, no_header_file)
        columns = ["A", "B", "C", "D", "E"]
        df = read_ods(path, 1, headers=False, columns=columns)
        assert list(df.columns) == columns
        assert len(df) == 10

    def test_duplicated_column_names(self):
        path = os.path.join(rsc, duplicated_column_names_file)
        df = read_ods(path, 1)
        assert isinstance(df, pd.DataFrame)
        assert len(df.columns) == 4
        assert "website.1" in df.columns

    def test_header_file_col_len(self):
        path = os.path.join(rsc, col_len_file)
        df = read_ods(path, 1)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 10
        assert (len(df.columns) == 5)

    def test_wrong_id_type(self):
        path = os.path.join(rsc, header_file)
        with pytest.raises(ValueError) as e_info:
            read_ods(path, 1.0)
            assert e_info.match("Sheet id has to be either `str` or `int`")

    def test_non_existent_sheet(self):
        path = os.path.join(rsc, header_file)
        sheet_name = "No_Sheet"
        with pytest.raises(ValueError) as e_info:
            read_ods(path, sheet_name)
            assert e_info.match(f"There is no sheet named {sheet_name}")

    def test_missing_header(self):
        path = os.path.join(rsc, missing_header_file)
        df = read_ods(path, 1)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 10
        assert (len(df.columns) == 5)
        assert df.columns[2] == "unnamed.1"
