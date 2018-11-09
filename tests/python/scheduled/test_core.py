import datetime
import os

from pandas import DataFrame
from context import utils
from context import formatters


def test_load_profile_contains_mapping():
    # test that the mapping section exists
    filename = os.path.join(utils.DATA_DIR, "BankOfOklahoma.yaml")

    assert os.path.exists(filename)

    profile = utils.load_profile(filename)

    assert profile.get("mapping") is not None


def test_columns_are_mapped():
    profile = {
        "mapping": {
            "amount": "Cost",
            "date": "Date",
            "security name": "Ticker",
            "shares": "Quantity",
            "transaction price": "Cash",
            "transaction type": "Description",
        }
    }

    data = [
        [
            209.95,
            datetime.date(year=2018, month=11, day=7),
            "AAPL",
            1.0,
            -209.95,
            "Purchase",
        ]
    ]
    df = DataFrame(
        data,
        columns=["Cost", "Date", "Ticker", "Quantity", "Cash", "Description"],
    )
    renamed_df = formatters.rename_cols(df, mapping=profile.get('mapping'))
    assert list(renamed_df.columns) == [
        "amount",
        "date",
        "security name",
        "shares",
        "transaction price",
        "transaction type",
    ]


def test_failing_test():
    STRUCT = [
        "date",
        "security name",
        "transaction type",
        "shares",
        "transaction price",
        "amount",
    ]

    data = [
        [
            209.95,
            datetime.date(year=2018, month=11, day=7),
            "AAPL",
            1.0,
            -209.95,
            "Purchase",
        ]
    ]

    df = DataFrame(
        data,
        columns=[
            "amount",
            "date",
            "security name",
            "shares",
            "transaction price",
            "transaction type",
        ],
    )

    reordered_df = formatters.subset_and_order(df)
    assert list(reordered_df.columns) == STRUCT
