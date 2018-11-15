import sys

from pandas import DataFrame


def load_plugins(plugins):
    plugin_module = sys.modules[__name__]
    return [getattr(plugin_module, plugin) for plugin in plugins]


def bank_of_oklahoma(df: DataFrame):
    """Replace the values of the transaction type column with the first word."""
    df["transaction type"] = df["transaction type"].apply(lambda x: x.split(" ", 1)[0])
    return df


def dummy_plugin(name):
    return f"Hello, {name}!"
