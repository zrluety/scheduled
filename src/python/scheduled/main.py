import os

import pandas as pd
import yaml

from pandas import DataFrame

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))

RESOURCES_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "resources")
)


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
    """Finds the path to the correct file given name"""
    for file in os.listdir(DATA_DIR):
        filename = os.path.join(DATA_DIR, file)
        with open(filename, "r") as y:
            profile = yaml.load(y)

            if profile.get("name") == name:
                return filename

    # if name is not found, raise error.
    raise FileNotFoundError(f"No profile was found with the name {name}")


def extract_data(src, profile):
    """Extract data from src using profile."""
    _, ext = os.path.splitext(src)

    if ext == ".csv":
        pandas_args = get_pandas_args(profile)
        transaction_data = pd.read_csv(src, **pandas_args)
    elif ext == ".xlsx" or ".xls":
        pandas_args = get_pandas_args(profile)
        transaction_data = pd.read_excel(src, **pandas_args)
    else:
        raise ValueError("Unsupported file extension")

    return transaction_data


def get_pandas_args(profile):
    """Get the pandas arguments from profile."""
    pandas_args = profile.get("options").get("pandas")

    if pandas_args is None:
        pandas_args = {}

    return pandas_args


def save(transaction_data, dst):
    """Save transaction_data to dst."""
    writer = pd.ExcelWriter(dst)
    transaction_data.to_excel(
        writer, "Transactions", index=False, header=False
    )


def rename_cols(df: DataFrame, profile):
    """Map columns to the standard template."""
    old_names = profile.get("mapping").values()
    new_names = profile.get("mapping").keys()

    return df.rename(index=str, columns=dict(zip(old_names, new_names)))


def reorder_cols(df: DataFrame):
    """Order columns to standard template."""
    return df[
        [
            "date",
            "security name",
            "transaction type",
            "shares",
            "transaction price",
            "amount",
        ]
    ]
