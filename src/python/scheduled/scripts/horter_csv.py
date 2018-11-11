from io import StringIO

from pandas import read_csv, concat, DataFrame, ExcelWriter
from pandas.io.common import EmptyDataError

from scheduled.parser import ScheduleDCsvParser
from scheduled.utils import extract_tables
from scheduled.utils import format_output

csv_file = r"C:\Users\zluety\Desktop\2017Q3 HIM560113-G8Forward.csv"
output_file = r"C:\Users\zluety\Desktop\2017Q3 HIM560113-G8Forward.xlsx"

# Horter options and mapping
options = {
    "v_align": "top",
    "fields": [
        "Date",
        "Activity",
        "Quantity",
        "Description",
        "Trade Execution Fee",
        "Other Fees",
        "Price",
        "Amount",
    ],
}

mapping = {
    "Date": "Date",
    "Description": "Security Name",
    "Activity": "Transaction Type",
    "Quantity": "Shares",
    "Price": "Transaction Price",
    "Amount": "Amount",
}


with ScheduleDCsvParser(csv_file, options=options) as raw_csv:
    try:
        tables = extract_tables(raw_csv, options.get("fields"))
        df = concat(
            [read_csv(StringIO("\r\n".join(table))) for table in tables]
        ).reset_index(drop=True)
    except EmptyDataError:
        df = DataFrame({"Empty": []})

if not df.empty:
    output_df = format_output(df, mapping)
    writer = ExcelWriter(output_file)
    output_df.to_excel(writer, "Sheet1", index=False, header=False)
    writer.save()
