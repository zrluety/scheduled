from io import StringIO

from pandas import read_csv, concat, DataFrame, ExcelWriter
from pandas.io.common import EmptyDataError

from scheduled.parser import ScheduleDCsvParser
from scheduled.utils import extract_tables
from scheduled.utils import format_output, read_profile

csv_file = r'G:\zluety\Programming\ScheduleD\csv_exctractions\06.csv'
profile_path = r'I:\TEAM_I\INSUR\Schedd_Macros\Python\scheduled\profiles\RBC.yaml'
output_file = r'G:\zluety\Programming\ScheduleD\xlsx_extractions\06.xlsx'

with open(profile_path) as f:
    y = read_profile(f)
    mapping = y.get('mapping')
    options = y.get('options')

with ScheduleDCsvParser(csv_file) as raw_csv:
    try:
        tables = extract_tables(raw_csv, options.get('fields'))
        df = concat([read_csv(StringIO('\r\n'.join(table))) for table in tables]).reset_index(drop=True)
    except EmptyDataError:
        df = DataFrame({'Empty': []})

if not df.empty:
    output_df = format_output(df, mapping)
    writer = ExcelWriter(output_file)
    output_df.to_excel(writer, 'Sheet1', index=False, header=False)
    writer.save()