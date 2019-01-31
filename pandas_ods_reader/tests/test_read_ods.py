import os

import pandas as pd

from pandas_ods_reader import read_ods


root = os.path.dirname(os.path.abspath(__file__))
rsc = os.path.join(root, "rsc")


class TestOdsReader(object):
    def test_header_file_with_int(self):
        example = "example_headers.ods"
        path = os.path.join(rsc, example)
        df = read_ods(path, 1)
        assert isinstance(df, pd.DataFrame)

    def test_header_file_with_str(self):
        example = "example_headers.ods"
        path = os.path.join(rsc, example)
        df = read_ods(path, "Sheet1")
        assert isinstance(df, pd.DataFrame)

    def test_no_header_file_no_cols(self):
        example = "example_no_headers.ods"
        path = os.path.join(rsc, example)
        df = read_ods(path, 1, headers=False)
        assert list(df.columns) == [
            "column_%s" % i for i in range(len(df.columns))]

    def test_no_header_file_with_cols(self):
        example = "example_headers.ods"
        path = os.path.join(rsc, example)
        columns = ["A", "B", "C", "D", "E"]
        df = read_ods(path, 1, headers=False, columns=columns)
        assert list(df.columns) == columns
