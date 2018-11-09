from pandas import ExcelWriter

from . import utils
from . import formatters

class Session:

    def __init__(self, profile):
        """Create a Schedule D
        
        Parameters
        ----------
        profile : str
            The name of the institution. The name of the institution is used
            to look up a configuration file containing values used to prepare
            the Schedule D transaction data.
        """
        self.profile = profile

        # options is a dictionary of values used to prepare the Schedule D
        # transaction data
        self.options = utils.load_profile(profile)

    def read(self, source):
        """Extract transaction data from client statement.
        
        Parameters
        ----------
        source : str
            Path to the statement file.
        
        """
        return utils.read(source, **self.options)

    def format(self, transaction_data):
        """Format the transaction data according to the Schedule D template.
        
        Parameters
        ----------
        transaction_data : DataFrame
            The transaction data
        
        """
        return formatters.format(transaction_data, **self.options)

    def save(self, transaction_data, dest):
        """Save the transaction data to a file.
        
        Parameters
        ----------
        transaction_data : DataFrame
            The transaction data. By the time you are saving the file, the
            transaction data should match the Schedule D template.
        dest : str
            Path to save the file to.
        
        """
        writer = pd.ExcelWriter(dst)
        transaction_data.to_excel(
            writer, "Transactions", index=False, header=False
        )
