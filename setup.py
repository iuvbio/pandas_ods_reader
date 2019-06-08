from setuptools import setup, find_packages


VERSION = "0.0.7"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="pandas_ods_reader",
      version=VERSION,
      description="Read in an ODS file and return it as a pandas.DataFrame",
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities",
      ],
      keywords="data io pandas ods",
      url="http://github.com/iuvbio/pandas_ods_reader",
      author="iuvbio",
      author_email="cryptodemigod@protonmail.com",
      license="MIT",
      packages=find_packages(),
      zip_safe=False,
      install_requires=["ezodf", "pandas", "lxml"],
      setup_requires=["pytest-runner"],
      tests_require=["pytest"]
      )
