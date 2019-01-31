import os

import pandas as pd

from pandas_ods_reader import read_ods


root = os.path.dirname(os.path.abspath(__file__))
rsc = os.path.join(root, "rsc")

header_file = "example_headers.ods"
no_header_file = "example_no_headers.ods"


class TestOdsReader(object):
    def test_header_file_with_int(self):
        path = os.path.join(rsc, header_file)
        df = read_ods(path, 1)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 10

    def test_header_file_with_str(self):
        path = os.path.join(rsc, header_file)
        df = read_ods(path, "Sheet1")
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 10

    def test_header_file_with_cols(self):
        path = os.path.join(rsc, header_file)
        columns = ["One", "Two", "Three", "Four", "Five"]
        df = read_ods(path, "Sheet1", columns=columns)
        assert list(df.columns) == columns
        assert len(df) == 10

    def test_no_header_file_no_cols(self):
        path = os.path.join(rsc, no_header_file)
        df = read_ods(path, 1, headers=False)
        assert list(df.columns) == [
            "column_%s" % i for i in range(len(df.columns))]
        assert len(df) == 10

    def test_no_header_file_with_cols(self):
        path = os.path.join(rsc, no_header_file)
        columns = ["A", "B", "C", "D", "E"]
        df = read_ods(path, 1, headers=False, columns=columns)
        assert list(df.columns) == columns
        assert len(df) == 10
