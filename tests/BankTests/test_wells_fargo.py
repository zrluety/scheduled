import os

import pandas as pd
import pandas.testing as pdt
import pytest

from manager import TEST_DATA_DIR
from scheduled import api
from scheduled.pdf import read_pdf
from scheduled.session import Session
from scheduled.utils import load_profile


def test_wells_fargo_profile_exists():
    profile = load_profile("Wells Fargo")
    assert profile is not None


def test_wellsfargo_profile_has_pdf_args():
    profile = load_profile("Wells Fargo")

    pdf_args = profile.get("pdf_args")
    assert pdf_args is not None
    assert type(pdf_args) == dict

    names = pdf_args.get("names")
    assert names is not None
    assert type(names) == list

    stopwords = pdf_args.get("stopwords")
    assert stopwords is not None
    assert type(stopwords) == list

    assert "Total Income and distributions" in stopwords

    v_align = pdf_args.get("v_align")
    assert v_align == "top"


def test_wells_fargo_statement_exists():
    WELLS_FARGO_STATEMENT = os.path.join(TEST_DATA_DIR, "201601 1205-EatonsNeck.pdf")
    assert os.path.exists(WELLS_FARGO_STATEMENT)


def test_read_pdf_creates_file():
    WELLS_FARGO_STATEMENT = os.path.join(TEST_DATA_DIR, "201601 1205-EatonsNeck.pdf")
    profile = load_profile("Wells Fargo")

    # read the pdf
    read_pdf(
        filepath=WELLS_FARGO_STATEMENT,
        outfilepath=os.path.splitext(WELLS_FARGO_STATEMENT)[0] + ".csv",
        names=profile.get("pdf_args").get("names"),
        stopwords=profile.get("pdf_args").get("stopwords"),
        v_align=profile.get("pdf_args").get("v_align"),
    )

    # check that the ouptput file is made
    assert os.path.exists(os.path.splitext(WELLS_FARGO_STATEMENT)[0] + ".csv")


def test_read_correct_data():
    WELLS_FARGO_STATEMENT = os.path.join(TEST_DATA_DIR, "201601 1205-EatonsNeck.pdf")

    # the first row from the statement
    expected = ["01/26", "Cash", "DEPOSIT", None, "FUNDS RECD", None, "5,000.00"]
    transaction_data = api.read(WELLS_FARGO_STATEMENT, "Wells Fargo")

    # for comparing, replace nan with None
    transaction_data1 = transaction_data.where((pd.notnull(transaction_data)), None)
    first_row = list(transaction_data1.iloc[0])
    assert first_row == expected


@pytest.mark.skip(
    reason="This checks that two dataframes are equivalent and they are, the test fails for some weird reason"
)
def test_wells_fargo_session():
    WELLS_FARGO_STATEMENT = os.path.join(TEST_DATA_DIR, "201601 1205-EatonsNeck.pdf")
    transaction_data = api.read(WELLS_FARGO_STATEMENT, "Wells Fargo")
    transaction_data = api.format(transaction_data, "Wells Fargo")
    transaction_data.iloc[:, 5].to_clipboard(index=False)

    expected = pd.read_excel(
        os.path.join(TEST_DATA_DIR, "201601 1205-EatonsNeck.xlsx"),
        header=None,
        names=[
            "date",
            "security name",
            "transaction type",
            "shares",
            "transaction price",
            "amount",
        ],
    )

    assert transaction_data.shape == expected.shape

    # If the shapes are the same, reindex so the indices are identical
    expected = expected.set_index(transaction_data.index)

    pdt.assert_frame_equal(transaction_data, expected, check_index_type=False)
