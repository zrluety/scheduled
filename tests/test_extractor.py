import os
from pandas import DataFrame
from pandas.util.testing import assert_frame_equal
import unittest
import xlsxwriter

from .context import extractor, TEST_ROOT, sample_csv


class TestExtractorBasic(unittest.TestCase):
    def setUp(self):
        """Create files used for testing"""
        workbook = xlsxwriter.Workbook(os.path.join(TEST_ROOT, 'tmp.xlsx'))
        worksheet = workbook.add_worksheet('Sheet1')

        # Some data we want to write to the worksheet.
        expenses = (
            ['aExpense', 'bBudget'],
            ['Rent', 1000],
            ['Gas', 100],
            ['Food', 300],
            ['Gym', 50],
        )

        # Start from the first cell. Rows and columns are zero indexed.
        row = 0
        col = 0

        # Iterate over the data and write it out row by row.
        for item, cost in (expenses):
            worksheet.write(row, col, item)
            worksheet.write(row, col + 1, cost)
            row += 1

        workbook.close()

    def tearDown(self):
        """Remove temp files used for tests"""
        os.remove(os.path.join(TEST_ROOT, 'tmp.xlsx'))

    def test_extractor_factory(self):
        """Extractor class includes a static factory method for returning Extractors."""
        e = extractor.Extractor.factory('.csv')
        self.assertTrue(isinstance(e, extractor.CsvExtractor))

    def test_xlsx_extract(self):
        """Options passed from _given_profile to extractor should be used properly."""
        e = extractor.ExcelExtractor()
        xlsx_file = os.path.join(TEST_ROOT, 'tmp.xlsx')
        options = {'sheetname': 'Sheet1'}

        df = e.extract(xlsx_file, options)

        expected_df = DataFrame(
            {"aExpense": ['Rent', 'Gas', 'Food', 'Gym'],
             "bBudget": [1000, 100, 300, 50]}, )
        assert_frame_equal(df, expected_df)

    def test_csv_extract_with_options(self):
        """Options passed from _given_profile to extractor should be used properly."""

        options = {'header': 1}
        e = extractor.CsvExtractor()
        df = e.extract(sample_csv, options)
        headers = list(df)

        self.assertEqual(headers, ['f1', 'f2'])

    def test_raise_not_implemented_on_base_extract(self):
        """The base extractor class should raise a NotImplementedError when extract is called."""

        e = extractor.Extractor()

        with self.assertRaises(NotImplementedError):
            e.extract('/tmp/fake/source.csv')
