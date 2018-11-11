import os
import sys

# Setup environment
TEST_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
PROJECT_ROOT = os.path.dirname(TEST_ROOT)
PACKAGE_ROOT = os.path.join(PROJECT_ROOT, "src", "python")
sys.path.insert(0, PACKAGE_ROOT)

import scheduled.session as session


def test_bank_of_oklahoma():
    s = session.Session("Bank Of Oklahoma")
    transaction_data = s.read(
        os.path.join(TEST_ROOT, 'scheduled', 'IntegrationTests', 'bok.xlsx')
    )

    # check data is read from the source file
    assert not transaction_data.empty

    transaction_data = s.format(transaction_data)
    # verify that the columns are in the write order
    assert list(transaction_data.columns) == [
        "date",
        "security name",
        "transaction type",
        "shares",
        "transaction price",
        "amount",
    ]
