pandas-ods-reader
===

Provides a function to read in a **.ods** or **.fods** file and returns a pandas DataFrame.

It uses `ezodf` to read in **.ods** files. Since **.fods** files are essentially xml, `lxml` is used to read them. The correct parser is automatically chosen based on the file's extension.

If a range is specified in the sheet to be imported, it seems that `ezodf` imports empty cells as well. Therefore, completely empty rows and columns are dropped from the DataFrame, before it is returned. Only trailing empty rows and columns are dropped.

If the ODS file contains duplicated column names, they will be numbered and the number is appended to the column name in the resulting DataFrame.

Dependencies
---

-   `ezodf`
-   `lxml`
-   `pandas`

Installation
---

`pip install pandas-ods-reader`

Usage
---

```Python
from pandas_ods_reader import read_ods

path = "path/to/file.ods"

# by default the first sheet is imported
df = read_ods(path)

# load a sheet based on its index (1 based)
sheet_idx = 2
df = read_ods(path, sheet_idx)

# load a sheet based on its name
sheet_name = "sheet1"
df = read_ods(path, sheet_name)

# load a file that does not contain a header row
# if no columns are provided, they will be numbered
df = read_ods(path, 1, headers=False)

# load a file and provide custom column names
# if headers is True (the default), the header row will be overwritten
df = read_ods(path, 1, columns=["A", "B", "C"])
```
