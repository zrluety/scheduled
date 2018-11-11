from setuptools import setup, find_packages

setup(
    name="scheduled",
    version="0.2",
    packages=find_packages('src/python'),
    package_dir={'': 'src/python'},
    package_data={"scheduled": ["data/*"]},
    include_package_data=True,
    install_requires=["Click", "Pandas", "pyyaml", "xlrd", "xlsxwriter"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    entry_points="""
        [console_scripts]
        scheduled=scheduled.scripts.cli:cli
    """,
    author="Zachary Luety",
    author_email="zluety@gpwa.com",
    description="A package to simplify working with Schedule D",
    url="https://github.com/zrluety/scheduled"
)
