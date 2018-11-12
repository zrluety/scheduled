import codecs
import os
import sys

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

about = {}

with open(os.path.join(here, "src", "python", "scheduled", "__version__.py")) as f:
    exec(f.read(), about)

required = [
    "pandas>=0.23.4",
    "openpyxl>=2.5.9",
    "xlsxwriter>=1.1.2",
    "xlrd>=1.1.0",
    "pyyaml>=3.13",
    "tabula-py>=1.3.1",
    "click>=7.0",
]

setup(
    name="scheduled",
    version=about["__version__"],
    description="Rapid Schedule D Completion",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Zachary Luety",
    author_email="zluety@gpwa.com",
    url="https://github.com/zrluety/scheduled",
    packages=find_packages("src/python"),
    entry_points={
        "console_scripts": [
            "scheduled=scheduled.scripts.cli:cli"
        ]
    },
    package_dir={"": "src/python"},
    package_data={
        "": ["LICENSE"],
        "scheduled": ["data/*"],
    },
    include_package_data=True,
    python_requires=">=3.5",
    install_requires=required,
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    license="MIT"
)
