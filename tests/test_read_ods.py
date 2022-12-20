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
skiprows_file = "example_skiprows.ods"


@pytest.mark.parametrize("suffix", [".ods", ".fods"])
def test_header_file_simple(suffix: str) -> None:
    """Test a simple file with headers."""
    path = rsc / header_file
    df = read_ods(path.with_suffix(suffix))

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 10
    assert len(df.columns) == 5


@pytest.mark.parametrize("suffix", [".ods", ".fods"])
def test_header_file_with_int(suffix: str) -> None:
    """Test referencing a sheet by index."""
    path = rsc / header_file
    df = read_ods(path.with_suffix(suffix), 1)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 10
    assert len(df.columns) == 5


@pytest.mark.parametrize("suffix", [".ods", ".fods"])
def test_header_file_with_str(suffix: str) -> None:
    """Test referencing a sheet by name."""
    path = rsc / header_file
    df = read_ods(path.with_suffix(suffix), "Sheet1")

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 10
    assert len(df.columns) == 5


@pytest.mark.parametrize("suffix", [".ods", ".fods"])
def test_header_file_with_cols(suffix: str) -> None:
    """Test overwriting haders with column names."""
    path = rsc / header_file
    columns = ["One", "Two", "Three", "Four", "Five"]
    df = read_ods(path.with_suffix(suffix), "Sheet1", columns=columns)

    assert list(df.columns) == columns
    assert len(df) == 10
    assert len(df.columns) == 5


@pytest.mark.parametrize("suffix", [".ods", ".fods"])
def test_no_header_file_no_cols(suffix: str) -> None:
    """Test autogeneration of headers with no headers and not column names."""
    path = rsc / no_header_file
    df = read_ods(path.with_suffix(suffix), 1, headers=False)

    assert list(df.columns) == [f"column.{i}" for i in range(len(df.columns))]
    assert len(df) == 10
    assert len(df.columns) == 5


@pytest.mark.parametrize("suffix", [".ods", ".fods"])
def test_no_header_file_with_cols(suffix: str) -> None:
    """Test reading a file with no headers and passing column names."""
    path = rsc / no_header_file
    columns = ["A", "B", "C", "D", "E"]
    df = read_ods(path.with_suffix(suffix), 1, headers=False, columns=columns)

    assert list(df.columns) == columns
    assert len(df) == 10


@pytest.mark.parametrize("suffix", [".ods", ".fods"])
def test_duplicated_column_names(suffix: str) -> None:
    """Test numbering duplicate column names."""
    path = rsc / duplicated_column_names_file
    df = read_ods(path.with_suffix(suffix), 1)

    assert isinstance(df, pd.DataFrame)
    assert len(df.columns) == 4
    assert "website.1" in df.columns


@pytest.mark.parametrize("suffix", [".ods", ".fods"])
def test_header_file_col_len(suffix: str) -> None:
    """Test the correct number of columns is read."""
    path = rsc / col_len_file
    df = read_ods(path.with_suffix(suffix), 1)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 10
    assert len(df.columns) == 5


@pytest.mark.parametrize("suffix", [".ods", ".fods"])
def test_wrong_id_type(suffix: str) -> None:
    """Verify passing a wrong id type raises an error."""
    path = rsc / header_file

    with pytest.raises(ValueError) as e_info:
        read_ods(path.with_suffix(suffix), 1.0)  # type: ignore[arg-type]
        assert e_info.match("Sheet id has to be either `str` or `int`")


@pytest.mark.parametrize("suffix", [".ods", ".fods"])
def test_non_existent_sheet(suffix: str) -> None:
    """Verify referencing a non-existent sheet raises an error."""
    path = rsc / header_file
    sheet_name = "No_Sheet"

    with pytest.raises(KeyError) as e_info:
        read_ods(path.with_suffix(suffix), sheet_name)
        assert e_info.match(f"There is no sheet named {sheet_name}")


@pytest.mark.parametrize("suffix", [".ods", ".fods"])
def test_missing_header(suffix: str) -> None:
    """Verify that a missing header is named."""
    path = rsc / missing_header_file
    df = read_ods(path.with_suffix(suffix), 1)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 10
    assert len(df.columns) == 5

    assert df.columns[2] == "unnamed.1"


@pytest.mark.parametrize("suffix", [".ods", ".fods"])
def test_mixed_dtypes(suffix: str) -> None:
    """Verify loading a df with mixed types."""
    path = rsc / mixed_dtypes_file
    df = read_ods(path.with_suffix(suffix), 1)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 10
    assert len(df.columns) == 5

    type_list = [float, object, float, float, object]
    assert df.dtypes.tolist() == type_list
    col_b_types = [type(v) for v in df.B.values]
    assert str in col_b_types and float in col_b_types


@pytest.mark.parametrize("suffix", [".ods", ".fods"])
def test_skiprows(suffix: str) -> None:
    """Verify skipping rows works correctly."""
    path = rsc / skiprows_file
    df = read_ods(path.with_suffix(suffix), skiprows=2)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 8
    assert len(df.columns) == 5
    assert df.columns.tolist() == ["a", "b", "c", "d", "e"]


def test_invalid_path() -> None:
    """Verify passing an invalid path raises an error."""
    path = rsc / "does-not-exist.ods"
    with pytest.raises(FileNotFoundError, match="does not exist"):
        read_ods(path)
