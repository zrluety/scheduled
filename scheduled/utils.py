import yaml
import os
from pandas import to_datetime

CONSTANTS = {
    'PROJECT_PATH': os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
    'JAR': os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'resources', 'jar',
                        'scheduled-1.0.jar'),
    'TMP': os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'resources', 'tmp')
}


def read_profile(stream):
    """Load and validate stream as a _given_profile."""
    y = yaml.load(stream)
    # _validatie_profile(y)
    return y


def _validatie_profile(y):
    """Ensure the _given_profile contains the necessary components.

    Every _given_profile MUST provide the following keys:
        method: how to extract the source data
        mapping: instructions to move from source format to output format

    Additionally, the following optional keys can be provided:
        options: method-specific options required for working with the source

    """

    required_keys = ['mapping']
    for key in required_keys:
        if key not in y:
            raise KeyError('{key} is a required field.'.format(key))


def format_output(df, mapping):
    """Format output DataFrame"""
    df = remove_unmapped_columns(df, mapping)
    df = order_columns(df, mapping)
    df = order_by_first(df)
    name_columns(df, mapping)
    return df


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


def extract_tables(stream, fields):
    rows = stream.getvalue().split('\r\n')

    table = []
    tables = []

    for row in rows:
        # If we find every field int he field list in a row, we assume we have
        # found a header row. First load the current table into a dataframe,
        # then we begin building the next table.
        if all([field in row for field in fields]):

            # Load current table into frame if it exists
            if table:
                tables.append(table)
                table = []

        table.append(row)

    else:
        tables.append(table)

    return tables


def order_by_first(df):
    """Order the DataFrame based on the first-column"""

    cols = df.columns

    try:
        df['TEMP_SORT_COL'] = to_datetime(df[df.columns[0]], infer_datetime_format=True)
        df.sort_values(by='TEMP_SORT_COL', inplace=True)
    except:
        # This does not guarantee proper ordering if the date cannot be inferred from
        # the first column (this happens with Wells Fargo where the date is provided
        # in as month/day (e.g. 02/16). In the future we may want to check this using
        # regular expressions
        pass

    return df[cols]



