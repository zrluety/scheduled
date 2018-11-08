from setuptools import setup, find_packages

setup(
    name="scheduled",
    version="0.1",
    packages=["scheduled", "scheduled.scripts"],
    package_dir={"scheduled": "src/python/scheduled"},
    package_data={"scheduled": ["data/*.yaml"]},
    include_package_data=True,
    install_requires=["Click", "Pandas", "pyyaml", "xlrd", "xlsxwriter"],
    entry_points="""
        [console_scripts]
        scheduled=scheduled.scripts.cli:cli
    """,
)
