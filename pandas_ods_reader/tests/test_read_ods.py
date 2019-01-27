import os

from pandas_ods_reader import read_ods


root = os.path.dirname(os.path.abspath(read_ods.__file__))
test_dir = os.path.join(root, "tests")
