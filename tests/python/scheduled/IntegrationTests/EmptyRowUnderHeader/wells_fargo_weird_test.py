from io import StringIO

from pandas import read_csv, concat

import yaml
import pytest

from scheduled.parser import ScheduleDCsvParser
from scheduled.utils import extract_tables

# weird_wells_fargo_csv = (
#     r"G:\!Programs\scheduled\tests\IntegrationTests\EmptyRowUnderHeader\201702 "
#     r"1890-TTTDForrester.csv "
# )
# profile = r"G:\!Programs\scheduled\profiles\Wells Fargo_2.yaml"
# with open(profile) as f:
#     config = yaml.load(f)

# options = config.get("options")

# with ScheduleDCsvParser(weird_wells_fargo_csv, options) as stream:
#     tables = extract_tables(stream, options.get("fields"))
#     df = concat(
#         [read_csv(StringIO("\r\n".join(table))) for table in tables]
#     ).reset_index(drop=True)
#     df.to_csv("./wells_fargo_weird.csv")
