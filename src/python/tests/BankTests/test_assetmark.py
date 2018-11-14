import os

from manager import TEST_DATA_DIR
from scheduled.api import read
from scheduled.utils import load_profile
from scheduled.pdf import read_pdf


def test_assetmark_pdf_is_found():
    ASSETMARK_STATEMENT = os.path.join(TEST_DATA_DIR, "2015Q1 6073-ModernAuto.pdf")
    assert os.path.exists(ASSETMARK_STATEMENT)


def test_assetmark_profile_exists():
    profile = load_profile("AssetMark")
    assert profile is not None


def test_assetmark_profile_has_pdf_args():
    profile = load_profile("AssetMark")

    pdf_args = profile.get("pdf_args")
    assert pdf_args is not None
    assert type(pdf_args) == dict

    names = pdf_args.get("names")
    assert names is not None
    assert type(names) == list

    stopwords = pdf_args.get("stopwords")
    assert stopwords is not None
    assert type(stopwords) == list


def test_read_pdf_creates_file():
    ASSETMARK_STATEMENT = os.path.join(TEST_DATA_DIR, "2015Q1 6073-ModernAuto.pdf")
    profile = load_profile("AssetMark")

    # read the pdf
    read_pdf(
        filepath=ASSETMARK_STATEMENT,
        outfilepath=os.path.splitext(ASSETMARK_STATEMENT)[0] + ".csv",
        names=profile.get("pdf_args").get("names"),
        stopwords=profile.get("pdf_args").get("stopwords"),
        v_align=profile.get("pdf_args").get("v_align"),
    )

    # check that the ouptput file is made
    assert os.path.exists(os.path.splitext(ASSETMARK_STATEMENT)[0] + ".csv")


def test_csv_parser_reads_tables_into_dataframes():
    ASSETMARK_STATEMENT = os.path.join(TEST_DATA_DIR, "2015Q1 6073-ModernAuto.pdf")
    transaction_data = read(ASSETMARK_STATEMENT, "AssetMark")
    first_row = list(transaction_data.iloc[0])
    expected = [
        "01/02/15",
        "BlackRock Liquidity TempFund",
        "Purchase",
        "9,621.330",
        "$1.00",
        "-$9,621.33",
    ]
    assert first_row == expected
