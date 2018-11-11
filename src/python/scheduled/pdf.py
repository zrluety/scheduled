import os

class PdfExtractor:
    def __init__(self):
        self.jar = os.path.join


    def extract(self, source, options=None):

        o_file = os.path.join(
            CONSTANTS.get("TMP"), os.path.splitext(os.path.basename(source))[0] + ".csv"
        )

        if options.get("stopwords"):
            subprocess.run(
                [
                    "java",
                    "-jar",
                    CONSTANTS.get("JAR"),
                    source,
                    "-f",
                    ",".join(options.get("fields")),
                    "-s",
                    ",".join(options.get("stopwords")),
                    "-o",
                    o_file,
                ]
            )
        else:
            subprocess.run(
                [
                    "java",
                    "-jar",
                    CONSTANTS.get("JAR"),
                    source,
                    "-f",
                    ",".join(options.get("fields")),
                    "-o",
                    o_file,
                ]
            )

        with ScheduleDCsvParser(o_file, options) as raw_csv:
            try:
                tables = extract_tables(raw_csv, options.get("fields"))
                df = concat(
                    [read_csv(StringIO("\r\n".join(table))) for table in tables]
                ).reset_index(drop=True)
                return df
            except EmptyDataError:
                return DataFrame({"Empty": []})

