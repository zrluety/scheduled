import pandas as pd
import yaml


def load_profile(filename):
    """Load a bank profile from filename."""
    with open(filename, "r") as f:
        profile = yaml.load(f)

    return profile


def extract_data(src, profile):
    """Extract data from src using profile."""

    # read pandas args from profile
    pandas_args = profile.get("options").get("pandas")

    transaction_data = pd.read_excel(src, **pandas_args)

    return transaction_data
