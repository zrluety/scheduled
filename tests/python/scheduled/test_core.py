import os

from context import main


def test_load_profile_contains_mapping():
    # test that the mapping section exists
    filename = os.path.join(main.DATA_DIR, "BankOfOklahoma.yaml")

    assert os.path.exists(filename)

    profile = main.load_profile(filename)

    assert profile.get("mapping") is not None