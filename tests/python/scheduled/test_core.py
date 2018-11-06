import os

from scheduled.main import (
    load_profile,
    extract_data,
    PROFILES_DIR,
    RESOURCES_DIR,
    get_filename_from_name,
)


def test_load_profile_contains_mapping():
    # test that the mapping section exists
    filename = os.path.join(PROFILES_DIR, "BankOfOklahoma.yaml")

    assert os.path.exists(filename)

    profile = load_profile(filename)

    assert profile.get("mapping") is not None


def test_extract_Bank_of_Oklahoma():
    filename = os.path.join(PROFILES_DIR, "BankOfOklahoma.yaml")
    profile = load_profile(filename)

    src = os.path.join(RESOURCES_DIR, "ActivityListDownload20181012.xlsx")
    transaction_data = extract_data(src, profile)
    assert list(transaction_data.columns) == [
        "Date",
        "Ticker",
        "Security",
        "Description",
        "Cash",
        "Quantity",
        "Cost",
    ]


def test_get_filename_from_name():
    name = "Bank Of Oklahoma"
    assert (
        get_filename_from_name(name),
        r"C:\Users\gpwa\Projects\scheduled\profiles\BankOfOklahoma.yaml",
    )
