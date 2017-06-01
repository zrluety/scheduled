"""
tests.context.py
~~~~~~~~~~~~~~~~



"""

import os
import sys
from io import StringIO

# Setup environment
TEST_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(TEST_ROOT)
sys.path.insert(0, PROJECT_ROOT)

import scheduled
import scheduled.utils as utils
import scheduled.extractor as extractor
import scheduled.parser as parser
import scheduled.session as session


# An example YAML file that will be used for basic tests
sample_profile = """
method: read_csv
mapping: {f1: t1, f2: t2}

"""

bad_profile = """
method: read_csv

"""

# Sample csv file
sample_csv = StringIO("""A sample file with a description in the first row\nf1,f2\n1,2\n3,4\n""")