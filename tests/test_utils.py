import unittest

from pandas import DataFrame

from .context import scheduled, sample_profile, bad_profile


class TestProfiles(unittest.TestCase):
    def test_profile_load_method(self):
        """Test if _given_profile components load correctly."""
        profile = scheduled.utils.read_profile(sample_profile)
        self.assertEqual(profile['method'], 'read_csv')

    def test_profile_load_mapping(self):
        """Test if _given_profile components load correctly."""
        profile = scheduled.utils.read_profile(sample_profile)
        self.assertEqual(profile['mapping'], {'f1': 't1', 'f2': 't2'})

    def test_profile_fails_without_required_option(self):
        """Loading a _given_profile without required keys should raise an exception."""

        with self.assertRaises(KeyError):
            scheduled.utils.read_profile(bad_profile)


class TestOutputFunctions(unittest.TestCase):
    def test_name_columns(self):
        """The ouput DataFrame should be renamed with the mapped columns."""
        df = DataFrame(
            {"a": [1, 2, 3],
             "b": [4, 5, 6]})
        mapping = {'a': 'Col1', 'b': 'Col2'}

        scheduled.utils.name_columns(df, mapping)

        self.assertEqual(list(df), ['Col1', 'Col2'])

    def test_name_columns_ordering_maintained(self):
        """The ouput DataFrame should be renamed with the mapped columns.

        The ordering of the renamed DataFrame should not be changed. Even if
        the renamed columns are no longer in alphanumeric order.
        """
        df = DataFrame(
            {"a": [1, 2, 3],
             "b": [4, 5, 6]})
        mapping = {'a': 'z', 'b': 'y'}

        scheduled.utils.name_columns(df, mapping)

        self.assertEqual(list(df), ['z', 'y'])

    def test_name_columns_not_all_mapped(self):
        """The ouput DataFrame should be renamed with the mapped columns.

        A mapping does not have to be provided for each field in the original
        DataFrame.
        """
        df = DataFrame(
            {"a": [1, 2, 3],
             "b": [4, 5, 6],
             "c": [7, 8, 9]})
        mapping = {'a': 'Col1', 'b': 'Col2'}

        scheduled.utils.name_columns(df, mapping)

        self.assertEqual(list(df), ['Col1', 'Col2', 'c'])

    def test_name_columns_no_name_change(self):
        """The ouput DataFrame should be renamed with the mapped columns.

        Some DataFrames may already have the desired column names
        """
        df = DataFrame(
            {"a": [1, 2, 3],
             "b": [4, 5, 6]})
        mapping = {'a': 'a', 'b': 'b'}

        scheduled.utils.name_columns(df, mapping)

        self.assertEqual(list(df), ['a', 'b'])

    def test_order_columns(self):
        """Columns should be ordered according to the mapping.

        The field name mappings should be ordered in the way the output is
        desired.
        """

        # Original DataFrame is ordered ['a', 'b']
        df = DataFrame(
            {"a": [1, 2, 3],
             "b": [4, 5, 6]})
        mapping = {'b': 'b', 'a': 'a'}

        df = scheduled.utils.order_columns(df, mapping)

        self.assertEqual(list(df), ['b', 'a'])

    def test_order_columns_not_all_mapped(self):
        """Columns should be ordered according to the mapping.

        The field name mappings should be ordered in the way the output is
        desired. Unmapped fields are appended to the right of the DataFrame
        """

        # Original DataFrame is ordered ['a', 'b', 'c']
        df = DataFrame(
            {"a": [1, 2, 3],
             "b": [4, 5, 6],
             "c": [7, 8, 9]})
        mapping = {'c': 'Col1', 'b': 'Col2'}

        df = scheduled.utils.order_columns(df, mapping)

        self.assertEqual(list(df), ['c', 'b', 'a'])

    def test_remove_unmapped_columns(self):
        """Fields that are not mapped should be excluded from the output DataFrame."""

        df = DataFrame(
            {"a": [1, 2, 3],
             "b": [4, 5, 6],
             "c": [7, 8, 9]})

        # No mapping given for column 'c'
        mapping = {'a': 'a', 'b': 'b'}

        df = scheduled.utils.remove_unmapped_columns(df, mapping)

        self.assertEqual(list(df), ['a', 'b'])