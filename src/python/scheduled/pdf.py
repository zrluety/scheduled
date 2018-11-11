import os
import subprocess

from .parser import ScheduleDCsvParser

SCHEDULED_JAR = os.path.join(os.path.dirname(__file__), 'data', 'scheduled-1.1.jar')

def read_pdf(filepath, outfilepath, fields, stopwords, **kwargs):
    if options.get("stopwords"):
        subprocess.run(
            [
                "java",
                "-jar",
                SCHEDULED_JAR,
                filepath,
                "-f",
                ",".join(fields),
                "-s",
                ",".join(stopwords),
                "-o",
                outfilepath,
            ]
        )
    else:
        subprocess.run(
            [
                "java",
                "-jar",
                SCHEDULED_JAR,
                filepath,
                "-f",
                ",".join(fields),
                "-o",
                outfilepath,
            ]
        )

    with ScheduleDCsvParser(outfilepath, options) as raw_csv:
        try:
            tables = extract_tables(raw_csv, options.get("fields"))
            df = concat(
                [read_csv(StringIO("\r\n".join(table))) for table in tables]
            ).reset_index(drop=True)
            return df
        except EmptyDataError:
            return DataFrame({"Empty": []})


def extract_tables(stream, fields):
    rows = stream.getvalue().split("\r\n")

    table = []
    tables = []

    for row in rows:
        # If we find every field int he field list in a row, we assume we have
        # found a header row. First load the current table into a dataframe,
        # then we begin building the next table.
        if all([field in row for field in fields]):

            # Load current table into frame if it exists
            if table:
                tables.append(table)
                table = []

        table.append(row)

    else:
        tables.append(table)

    return tables