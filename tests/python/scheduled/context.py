import os
import sys

# Setup environment
TEST_ROOT = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
)
PROJECT_ROOT = os.path.dirname(TEST_ROOT)
PACKAGE_ROOT = os.path.join(PROJECT_ROOT, "src", "python")
sys.path.insert(0, PACKAGE_ROOT)

import scheduled
import scheduled.main as main

# import scheduled.utils as utils
# import scheduled.extractor as extractor
# import scheduled.parser as parser
# import scheduled.session as session
