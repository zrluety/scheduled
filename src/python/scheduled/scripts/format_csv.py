from io import StringIO

from pandas import read_csv, concat, DataFrame, ExcelWriter
from pandas.io.common import EmptyDataError

from scheduled.parser import ScheduleDCsvParser
from scheduled.utils import extract_tables
from scheduled.utils import format_output, read_profile

csv_file = r"C:\Users\zluety\Desktop\201712 VV RBC Trust Stmt.csv"
output_file = r"C:\Users\zluety\Desktop\201712 VV RBC Trust Stmt.xlsx"

# mock profile options
options = {
    "v_align": "top",
    "fields": [
        "Date",
        "Quantity",
        "Description",
        "Security Name",
        "Receipt",
        "Disb",
    ],
}

mapping = {
    "Date": "Date",
    "Security Name": "Security Name",
    "Description": "Transaction Type",
    "Quantity": "Shares",
    "Receipt": "Transaction Price",
    "Disb": "Amount",
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
