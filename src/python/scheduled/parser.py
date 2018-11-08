import csv
from io import StringIO
from itertools import zip_longest


# TODO: remove passing file, should use self.file


def isheader(full_row, fields):
    """Return true if full_row has each field (ignore blank headers)."""
    # blank columns may come in on the headers, we want to ignore these for
    # the comparison
    r_set = set([col for col in full_row if col != ""])
    f_set = set(fields)
    return r_set == f_set


class ScheduleDCsvParser:
    """ScheduleDCsvParser correctly handles csvs with coming from the SchduleD Extraction.
    
    A multiline csv file can contain multiple lines that correspond to the same
    row of data. e.g.
    
        "6/26/1997", "J.K. Rowling", "Harry Potter and the"
        "","","Sorcerer's Stone"
        
    is really a single entry of data.
    
        "6/26/1997", "J.K. Rowling", "Harry Potter and the Sorcerer's Stone"
    
    When read with the MultiLineCsv Class, the data above would be returned as
    a single row.
    
    Args:
        filename (str): The name of the file to read
    """

    def __init__(self, filename, options):
        try:
            self.file = open(filename)
        except TypeError:
            # Allow reader to accept IO object
            self.file = filename
        self.stream = StringIO()
        # call the appropriate csv parsing/combining algorithm
        if options.get("v_align") == "center":
            self.parse_vertically_centered_rows(self.file)
        else:
            self.merge_rows(self.file, options)

        self.file.close()

    def __enter__(self):
        return self.stream

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stream.close()

    def merge_rows(self, file, options):
        """Reads the given multiline csv file into a properly formatted StringIO.
        
        Args:
            file (IO): The multiline csv file to read.
        """
        reader = csv.reader(file, delimiter=",", quotechar='"')
        writer = csv.writer(self.stream, quoting=csv.QUOTE_NONNUMERIC)
        full_row = None

        # If a row does not contain data in the first column, the row
        # is joined with the nearest row above that does contain data.
        for row in reader:
            # If the first row is incomplete, there is no complete row to
            # append to so we must just accept it as an incomplete data row
            if full_row is None:
                if len(row[0]) > 0:
                    full_row = row
                else:
                    writer.writerow(row)
                continue

            # If the row is complete, write any prior stored complete row and update
            # full row.
            if len(row[0]) > 0:
                if full_row:
                    writer.writerow(full_row)
                full_row = row
            # TODO: prevent appending to header rows, this messes up pandas unioning method.
            # If the row is incomplete, append it to nearest above complete row.
            else:
                if isheader(full_row, options.get("fields")):
                    # This prevents appending to a header row but also loses the data in
                    # the current row. This should be changed to merge to the row within the
                    # prior table.
                    continue
                else:
                    combined_tup = list(
                        zip_longest(full_row, row, fillvalue="")
                    )
                    full_row = [
                        " ".join(content).strip() for content in combined_tup
                    ]
        else:
            # if full_row is None we are working with a blank source file and we
            # can raise an EmptyDataError
            if full_row:
                writer.writerow(full_row)

    def parse_vertically_centered_rows(self, file):
        """Correctly merge rows from csv output of vertically centered PDFs.

        We are making a few assumptions to get this to work. First we assume that there are
        at most 3 "nested rows" belonging to the single Row of data in the csv. Next we assume
        the leftmost column is going to be a single row.

        e.g.
            Col1,Col2,Col3
            r1c1,r1c2,r1c3
            ,r2c2a,             <- These pieces make up row 2
            r2c1,,r2c3          <- These pieces make up row 2
            ,r2c2b,             <- These pieces make up row 2
            r3c1,r3c2,r3c3

        Args:
            file (IO): the csv string to parse.
        Returns:
            A StringIO object containing the standardized csv data.
        """

        # load IO into reader
        reader = csv.reader(file, delimiter=",", quotechar='"')
        # writer will hold the new data
        writer = csv.writer(self.stream, quoting=csv.QUOTE_NONNUMERIC)

        # Because of our assumptions, we can only be in three states: 1) at the center axis
        # 2) one row above the center axis or 3) one row below the center axis.

        stored_row = (
            []
        )  # container that will hold data above the center row until it is merged with the center row.
        partial = (
            False
        )  # indicator if we are still waiting for more data for the row
        csv_row = []  # row that we will write to our output
        STATE = 1  # current state

        for row in reader:
            # at the center axis. Here we want to collect all of the data that is above the
            # center axis and merge it into our row.
            if len(row[0]) > 0:
                # We are moving from state one to state one, we simply write the row as both
                # rows are full data columns
                if STATE == 1:
                    writer.writerow(row)

                # merge data from above the center axis into the center row
                if len(stored_row) > 0:
                    # combine the contents column-wise.
                    it = zip_longest(stored_row.pop(), row, fillvalue="")
                    # create a new csv row.
                    csv_row.append(
                        [" ".join(content).strip() for content in it]
                    )
                    partial = True

                STATE = 1
            else:
                # If we are in State 1 (at the center row), there are two possible
                # scenerios. 1) we just transitioned from a Row with no nested rows
                # or 2) we are below the center row.
                #
                # For scenerio 2, the partial indicator will be set to True
                if STATE == 1:
                    # scenerio 2
                    if partial:
                        # merge data from below the center axis into the center row
                        it = zip_longest(csv_row.pop(), row, fillvalue="")
                        csv_row.append(
                            [" ".join(content).strip() for content in it]
                        )
                        # Add the row to the writer
                        writer.writerow(csv_row.pop())

                        partial = False

                        # We can bypass switching to state 3 because we always write a row
                        # at state 3 so there is no need to capture state 3 then write then
                        # transition to state 1.
                        STATE = 1
                    # scenerio 1
                    else:
                        stored_row.append(row)
                        partial = True
                        STATE = 2

                # If we are in state 3 (below the center axis). We must be at the row
                # above the next center axis. Store this data to be merged with the next
                # centered axis and transition to state 2.
                elif STATE == 3:
                    # store data from above the center axis to be merged into the center row
                    stored_row.append(row)

                    STATE = 2
