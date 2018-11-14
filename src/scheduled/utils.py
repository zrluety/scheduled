import os

import yaml
from pandas import read_csv, read_excel, to_datetime
from .pdf import read_pdf

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def load_profile(name):
    """Load a bank profile from filename."""
    filename = _get_filename_from_name(name)
    with open(filename, "r") as f:
        options = yaml.load(f)

    return options


def read(source, pandas_args=None, pdf_args=None, **kwargs):
    """Extract transaction data from client statement
    
    Parameters
    ----------
    source : str
        Path to statement file.
    pandas_args : dict, optional
        A dictionary of optional arguments to pass to the pandas_args read method
        (the default is None, which will use the default arguments for reading
        the file).
    
    """
    base, ext = os.path.splitext(source)

    if pandas_args is None:
        pandas_args = {}

    if ext == ".csv":
        transaction_data = read_csv(source, **pandas_args)

    elif ext == ".xlsx" or ext == ".xls":
        transaction_data = read_excel(source, **pandas_args)

    elif ext == ".pdf":

        if pdf_args is None:
            pdf_args = {}

        transaction_data = read_pdf(source, base + ".csv", **pdf_args)
    else:
        raise ValueError("Unsupported file type")

    return transaction_data


def _get_filename_from_name(name):
    """Finds the path to the correct file given name"""
    for file in os.listdir(DATA_DIR):
        # Ignore non yaml files
        if not file.endswith(".yaml"):
            continue

        filename = os.path.join(DATA_DIR, file)
        with open(filename, "r") as y:
            profile = yaml.load(y)

            if profile.get("name") == name:
                return filename

    # if name is not found, raise error.
    raise FileNotFoundError(f"No profile was found with the name {name}")


# These is the expected structure of the output dataframe
STRUCT = [
    "Date",
    "Security Name",
    "Transaction Type",
    "Shares",
    "Transaction Price",
    "Amount",
]

CONSTANTS = {
    "PROJECT_PATH": os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
    "JAR": os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
        "resources",
        "jar",
        "scheduled-1.1.jar",
    ),
    "TMP": os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))), "resources", "tmp"
    ),
}


def format_output(df, mapping):
    """Format output DataFrame"""
    df = remove_unmapped_columns(df, mapping)
    df = order_columns(df, mapping)
    df = order_by_first(df)
    name_columns(df, mapping)
    df = include_missing_columns(df)
    return df[STRUCT]


def remove_unmapped_columns(df, mapping):
    """Only keep the fields that should be in the output."""

    # Field names that should be kept
    keep_fields = list(mapping)

    return df[keep_fields]


def order_columns(df, mapping):
    """Reorder DataFrame columns from mapping"""
    # Field names in original DataFrame
    fields = list(df)

    # Ordered field names, note that not all columns will be mapped so we must
    # get the list of unmapped columns.
    ordered_cols = list(mapping)
    unmapped_cols = [col for col in fields if col not in ordered_cols]

    ordered_df = df[ordered_cols + unmapped_cols]

    return ordered_df


def name_columns(df, mapping):
    """Rename the column names for a DataFrame"""
    df.rename(index=str, columns=mapping, inplace=True)


def order_by_first(df):
    """Order the DataFrame based on the first-column"""

    cols = df.columns

    try:
        df["TEMP_SORT_COL"] = to_datetime(df[df.columns[0]], infer_datetime_format=True)
        df.sort_values(by="TEMP_SORT_COL", inplace=True)
    except:
        # This does not guarantee proper ordering if the date cannot be inferred from
        # the first column (this happens with Wells Fargo where the date is provided
        # in as month/day (e.g. 02/16). In the future we may want to check this using
        # regular expressions
        pass

    return df[cols]


def include_missing_columns(df):
    """Inserts blank columns for any columns missing from the expected structure."""
    missing_columns = [col for col in STRUCT if col not in list(df)]

    # include the mising columns
    return df.reindex(columns=list(df) + missing_columns)
