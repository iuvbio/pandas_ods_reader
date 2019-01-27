from setuptools import setup, find_packages


VERSION = "0.0.1"

setup(name="pandas_ods_reader",
      version=VERSION,
      description="Read in an ODS file and return it as a pandas.DataFrame",
      url="http://github.com/iuvbio/pandas_ods_reader",
      author="iuvbio",
      author_email="",
      license="MIT",
      packages=find_packages(["pandas_ods_reader"]),
      zip_safe=False,
      install_requires=["ezodf", "pandas"])
