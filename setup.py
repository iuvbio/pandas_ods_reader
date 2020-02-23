
from setuptools import setup, find_packages


version = None
with open('pandas_ods_reader/__init__.py') as f:
    for line in f.readlines():
        if not line.startswith('__version__'):
            continue
        version = line.split(' = ')[1].strip()[1:-1]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="pandas_ods_reader",
      version=version,
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
      setup_requires=["pytest-runner"],  # TODO: remove pytest-runner
      tests_require=["pytest"]
      )
