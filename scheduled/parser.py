import csv
from io import StringIO
from itertools import zip_longest


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

    def __init__(self, filename, **options):
        try:
            self.file = open(filename)
        except TypeError:
            # Allow reader to accept IO object
            self.file = filename
        self.stream = StringIO()
        self.merge_rows(self.file)
        self.file.close()

    def __enter__(self):
        return self.stream

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stream.close()

    def merge_rows(self, file):
        """Reads the given multiline csv file into a properly formatted StringIO.
        
        Args:
            file (IO): The multiline csv file to read.
        """
        reader = csv.reader(file, delimiter=',', quotechar='"')
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
            # If the row is incomplete, append it to nearest above complete row.
            else:
                combined_tup = list(zip_longest(full_row, row, fillvalue=''))
                full_row = [' '.join(content).strip() for content in combined_tup]
        else:
            # if full_row is None we are working with a blank source file and we
            # can raise an EmptyDataError
            if full_row:
                writer.writerow(full_row)
