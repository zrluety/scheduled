from setuptools import setup, find_packages

setup(
    name='scheduled',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'pyyaml',
        'pandas',
    ],
    entry_points='''
        [console_scripts]
        extract=scheduled.scripts.cli:run_app
    ''',
)
