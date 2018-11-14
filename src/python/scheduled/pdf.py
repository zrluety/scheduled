import os
import subprocess
from io import StringIO

from pandas import concat, DataFrame, read_csv
from pandas.errors import EmptyDataError

from .parser import ScheduleDCsvParser

SCHEDULED_JAR = os.path.join(os.path.dirname(__file__), "data", "scheduled-1.1.jar")


def get_java_call(filepath, outfilepath, names, stopwords, v_align):
    call = [
        "java",
        "-jar",
        SCHEDULED_JAR,
        filepath,
        "-f",
        ",".join(names),
        "-s",
        ",".join(stopwords),
        "-o",
        outfilepath,
    ]
    return " ".join(call)


def read_pdf(filepath, outfilepath, names, stopwords, v_align):
    if stopwords:
        subprocess.run(
            [
                "java",
                "-jar",
                SCHEDULED_JAR,
                filepath,
                "-f",
                ",".join(names),
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
                ",".join(names),
                "-o",
                outfilepath,
            ]
        )

    with ScheduleDCsvParser(outfilepath, names, v_align) as raw_csv:
        try:
            tables = extract_tables(raw_csv, names)
            df = concat(
                [read_csv(StringIO("\r\n".join(table))) for table in tables]
            ).reset_index(drop=True)
            return df
        except EmptyDataError:
            return DataFrame({"Empty": []})


def extract_tables(stream, names):
    rows = stream.getvalue().split("\r\n")

    table = []
    tables = []

    for row in rows:
        # If we find every field int he field list in a row, we assume we have
        # found a header row. First load the current table into a dataframe,
        # then we begin building the next table.
        if all([field in row for field in names]):

            # Load current table into frame if it exists
            if table:
                tables.append(table)
                table = []

        table.append(row)

    else:
        tables.append(table)

    return tables
