"""

scheduled.extractor
~~~~~~~~~~~~~~~~~~~

The extractor.py module contains the classes used to extract data from the source.
"""

from io import StringIO
import os
import subprocess

from pandas import read_csv, read_excel, concat, DataFrame
from pandas.io.common import EmptyDataError

from scheduled.parser import ScheduleDCsvParser
from scheduled.utils import CONSTANTS, extract_tables


class Extractor:
    """Base Extractor class."""

    @staticmethod
    def factory(ext):
        """Factory ext for creating extractor."""
        if ext.lower() == '.csv':
            return CsvExtractor()
        elif ext.lower() == '.xlsx':
            return ExcelExtractor()
        elif ext.lower() == '.pdf':
            return PdfExtractor()
        else:
            raise TypeError('{ext} is not a valid extraction ext'.format(ext))

    def extract(self, source, options=None):
        raise NotImplementedError


class CsvExtractor(Extractor):
    def __init__(self):
        super().__init__()

    def extract(self, source, options=None):
        if not options:
            options = {}
        df = read_csv(source)
        return df


class ExcelExtractor(Extractor):
    def __init__(self):
        super().__init__()

    def extract(self, source, options=None):
        if not options:
            options = {}

        df = read_excel(source)
        return df


class PdfExtractor(Extractor):
    def extract(self, source, options=None):

        o_file = os.path.join(CONSTANTS.get('TMP'), os.path.splitext(os.path.basename(source))[0] + '.csv')

        if options.get('stopwords'):
            subprocess.run(['java', '-jar', CONSTANTS.get('JAR'), source, '-f', ','.join(options.get('fields')),
                            '-s', ','.join(options.get('stopwords')), '-o', o_file])
        else:
            subprocess.run(['java', '-jar', CONSTANTS.get('JAR'), source, '-f', ','.join(options.get('fields')),
                            '-o', o_file])

        with ScheduleDCsvParser(o_file, options) as raw_csv:
            try:
                tables = extract_tables(raw_csv, options.get('fields'))
                df = concat([read_csv(StringIO('\r\n'.join(table))) for table in tables]).reset_index(drop=True)
                return df
            except EmptyDataError:
                return DataFrame({'Empty': []})
