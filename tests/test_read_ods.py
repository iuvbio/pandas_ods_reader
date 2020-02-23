"""Tests for core read_ods function with different files"""
from pathlib import Path

import pandas as pd
import pytest

from pandas_ods_reader import read_ods


root = Path(__file__).parent
rsc = root / "rsc"

header_file = "example_headers.ods"
no_header_file = "example_no_headers.ods"
duplicated_column_names_file = "example_duplicated_column_names.ods"
col_len_file = "example_col_lengths.ods"
missing_header_file = "example_missing_header.ods"
mixed_dtypes_file = "mixed_dtypes.ods"


class TestOdsReader:

    def test_header_file_simple(self):

        path = rsc / header_file
        df = read_ods(path)

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 10
        assert (len(df.columns) == 5)

    def test_header_file_with_int(self):

        path = rsc / header_file
        df = read_ods(path, 1)

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 10
        assert (len(df.columns) == 5)

    def test_header_file_with_str(self):

        path = rsc / header_file
        df = read_ods(path, "Sheet1")

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 10
        assert (len(df.columns) == 5)

    def test_header_file_with_cols(self):

        path = rsc / header_file
        columns = ["One", "Two", "Three", "Four", "Five"]
        df = read_ods(path, "Sheet1", columns=columns)

        assert list(df.columns) == columns
        assert len(df) == 10
        assert (len(df.columns) == 5)

    def test_no_header_file_no_cols(self):

        path = rsc / no_header_file
        df = read_ods(path, 1, headers=False)

        assert list(df.columns) == [
            f"column.{i}" for i in range(len(df.columns))]
        assert len(df) == 10
        assert (len(df.columns) == 5)

    def test_no_header_file_with_cols(self):

        path = rsc / no_header_file
        columns = ["A", "B", "C", "D", "E"]
        df = read_ods(path, 1, headers=False, columns=columns)

        assert list(df.columns) == columns
        assert len(df) == 10

    def test_duplicated_column_names(self):

        path = rsc / duplicated_column_names_file
        df = read_ods(path, 1)

        assert isinstance(df, pd.DataFrame)
        assert len(df.columns) == 4
        assert "website.1" in df.columns

    def test_header_file_col_len(self):

        path = rsc / col_len_file
        df = read_ods(path, 1)

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 10
        assert (len(df.columns) == 5)

    def test_wrong_id_type(self):

        path = rsc / header_file

        with pytest.raises(ValueError) as e_info:
            read_ods(path, 1.0)
            assert e_info.match("Sheet id has to be either `str` or `int`")

    def test_non_existent_sheet(self):

        path = rsc / header_file
        sheet_name = "No_Sheet"

        with pytest.raises(ValueError) as e_info:
            read_ods(path, sheet_name)
            assert e_info.match(f"There is no sheet named {sheet_name}")

    def test_missing_header(self):

        path = rsc / missing_header_file
        df = read_ods(path, 1)

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 10
        assert (len(df.columns) == 5)

        assert df.columns[2] == "unnamed.1"

    def test_mixed_dtypes(sefl):

        path = rsc / mixed_dtypes_file
        df = read_ods(path, 1)

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 10
        assert (len(df.columns) == 5)

        type_list = [float, object, float, float, object]
        assert df.dtypes.tolist() == type_list
        col_b_types = [type(v) for v in df.B.values]
        assert str in col_b_types and float in col_b_types
