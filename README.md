pandas_ods_reader
===

Provides a function to read in an ODS file and return a pandas DataFrame

Dependencies
---

- `ezodf`
- `lxml`
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
sheet_name = "sheet"
df2 = read_ods(path, sheet_name)
```
