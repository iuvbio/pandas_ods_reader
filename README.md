pandas_ods_reader
===

Provides a function to read in an ODS file and return a pandas DataFrame.

It uses `ezodf` to read in the ods file. If a range is specified in the sheet
to be imported, it seems that `ezodf` imports empty cells as well. Therefore,
all completely empty rows and columns are dropped from the DataFrame, before
it is returned.

Dependencies
---

- `ezodf`
- `pandas`

Installation
---

`pip install pandas_read_ods`

Usage
---

```Python
from pandas_ods_reader import read_ods

path = "path/to/file.ods"
sheet_idx = 1
df1 = read_ods(path, sheet_idx)
sheet_name = "sheet1"
df2 = read_ods(path, sheet_name)
```
