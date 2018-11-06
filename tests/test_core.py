import os

from scheduled.main import load_profile, extract_data

PROFILES_DIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'profiles')
)

RESOURCES_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'resources')
)


def test_load_profile_contains_mapping():
    # test that the mapping section exists
    filename = os.path.join(PROFILES_DIR, 'BankOfOklahoma.yaml')
    
    assert(os.path.exists(filename))

    profile = load_profile(filename)

    assert(profile.get('mapping') is not None)


def test_extract_Bank_of_Oklahoma():
    filename = os.path.join(PROFILES_DIR, 'BankOfOklahoma.yaml')
    profile = load_profile(filename)

    src = os.path.join(RESOURCES_DIR, 'ActivityListDownload20181012.xlsx')
    transaction_data = extract_data(src, profile)
    assert(list(transaction_data.columns) == [
        'Date',
        'Ticker',
        'Security',
        'Description',
        'Cash',
        'Quantity',
        'Cost',
    ])


    

    
