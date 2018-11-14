import os
import sys

from manager import TEST_DATA_DIR

import scheduled.session as session


def test_bank_of_oklahoma():
    s = session.Session("Bank Of Oklahoma")
    transaction_data = s.read(os.path.join(TEST_DATA_DIR, "bok.xlsx"))

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
