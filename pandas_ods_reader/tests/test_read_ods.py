import os
import sys

from pandas_ods_reader.read_ods import read_ods


root = os.path.dirname(os.path.abspath(__file__))


def test_header_file():
    example = "example_headers.ods"
    path = os.path.join(root, example)
    print("Test sheet by index")
    df = read_ods(path, 1)
    print(df)
    print("Test sheet by name")
    df = read_ods(path, "Sheet1")
    print(df)


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


def main():
    test_header_file()
    test_no_header_file()


if __name__ == "__main__":
    status = main()
    sys.exit(status)
