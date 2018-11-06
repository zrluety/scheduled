import os

import pandas as pd
import yaml

PROFILES_DIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "profiles")
)

RESOURCES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "resources"))


def run(name, src, dst):
    filename = get_filename_from_name(name)
    profile = load_profile(filename)
    transaction_data = extract_data(src, profile)
    save(transaction_data, dst)


def load_profile(filename):
    """Load a bank profile from filename."""
    with open(filename, "r") as f:
        profile = yaml.load(f)

    return profile


def get_filename_from_name(name):
    for file in os.listdir(PROFILES_DIR):
        filename = os.path.join(PROFILES_DIR, file)
        with open(filename, "r") as y:
            profile = yaml.load(y)

            if profile.get("name") == name:
                return filename

    # if name is not found, raise error.
    raise FileNotFoundError(f"No profile was found with the name {name}")


def extract_data(src, profile):
    """Extract data from src using profile."""

    # read pandas args from profile
    pandas_args = profile.get("options").get("pandas")
    if pandas_args is None:
        pandas_args = {}

    transaction_data = pd.read_excel(src, **pandas_args)

    return transaction_data


def save(transaction_data, dst):
    """Save transaction_data to dst."""
    writer = pd.ExcelWriter(dst)
    transaction_data.to_excel(writer, "Transactions", index=False, header=False)
