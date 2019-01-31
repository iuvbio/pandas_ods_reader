import os

import pandas as pd

from pandas_ods_reader import read_ods


root = os.path.dirname(os.path.abspath(__file__))


class OdsReaderTest(object):
    def test_header_file_with_int():
        example = "example_headers.ods"
        path = os.path.join(root, example)
        # print("Test sheet by index")
        df = read_ods(path, 1)
        assert isinstance(df, pd.DataFrame)

    def test_header_file_with_str():
        example = "example_headers.ods"
        path = os.path.join(root, example)
        df = read_ods(path, "Sheet1")
        print(df)
        assert isinstance(df, pd.DataFrame)

    def test_no_header_file():
        example = "example_no_headers.ods"
        path = os.path.join(root, example)
        print("Test sheet by index and default columns")
        df = read_ods(path, 1, headers=False)
        print(df)
        print("Test sheet by name and default columns")
        df = read_ods(path, "Sheet1", headers=False)
        print(df)
        print("Test sheet by index and specific columns")
        columns = ["A", "B", "C", "D", "E"]
        df = read_ods(path, 1, headers=False, columns=columns)
        print(df)
