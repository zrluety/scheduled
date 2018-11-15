from .plugins import load_plugins


def format(transaction_data, mapping, plugins=None, **kwargs):
    """Format the transaction data according to the Schedule D template.
    
    Parameters
    ----------
    transaction_data : DataFrame
        The transaction data
    mapping : dict
        A dictionary where the keys are the required column names for the
        template and the values are the existing column names.
    plugins : list, optional
        A list additional functions that should be run to get the data in the
        required template (the default is None, which means no additional
        formatting will be done.)
    
    """
    # Make a copy of the DataFrame prior to making any manipulations
    copy = transaction_data.copy()
    copy = rename_cols(copy, mapping)
    copy = subset_and_order(copy)

    if plugins is not None:
        for func in load_plugins(plugins):
            copy = func(copy)

    return copy


def rename_cols(transaction_data, mapping):
    """Rename columns to conform to Schedule D template.
    
    Parameters
    ----------
    transaction_data : DataFrame
        The transaction data
    mapping : dict
        A dictionary where the keys are the required column names for the
        template and the values are the existing column names.
    
    """
    old_names = mapping.values()
    new_names = mapping.keys()

    return transaction_data.rename(index=str, columns=dict(zip(old_names, new_names)))


def subset_and_order(transaction_data):
    """Order columns to standard template."""
    return transaction_data[
        [
            "date",
            "security name",
            "transaction type",
            "shares",
            "transaction price",
            "amount",
        ]
    ]
