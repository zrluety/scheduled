"""
Tables within the North Bay PDF cannot be extracted currently we we must use
the tabula tool to extract the values into CSV format. Once the values are
extracted we can use this application to format them to work with the
Schedule D tool.

"""
import pandas as pd

from io import StringIO
from scheduled.parser import ScheduleDCsvParser
from scheduled.utils import extract_tables


# the location of the csv file extracted from Tabula
csv = r"C:\Users\zluety\Downloads\tabula-201807 VV RBC Trust Stmt.csv"
xlsx = r"C:\Users\zluety\Downloads\tabula-201807 VV RBC Trust Stmt.xlsx"

# options are used to help format the data correctly
options = {
    'fields': ['Date',
               'Quantity',
               'Description',
               'Security Name',
               'Receipt',
               'Disb'],
}

# formats the csv to be so it can be used with the Schedule D tool
with ScheduleDCsvParser(csv, options) as raw_csv:
    tables = extract_tables(raw_csv, options.get('fields'))
    df = pd.concat([pd.read_csv(StringIO('\r\n'.join(table)))
                    for table in tables]).reset_index(drop=True)

    # safe output to excel
    writer = pd.ExcelWriter(xlsx)
    df.to_excel(writer, index=False)
    writer.save()
