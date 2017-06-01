import unittest
import logging

from .context import scheduled


# helper functions
def _get_lvl(logger):
    # Get int representation of log level
    lvl = logger.getEffectiveLevel()

    # Get text representation of log level
    s_lvl = logging.getLevelName(lvl)

    return s_lvl


class TestSessionBasic(unittest.TestCase):
    def test_develop_log_level(self):
        """The log level during develop should be debug."""
        # Create Session object.
        session = scheduled.Session(source='tmp/file.csv',
                                    profile='tmp_profile',
                                    scheduled='schd.xlsx',
                                    username='name',
                                    develop=True)

        self.assertEqual(_get_lvl(session._logger), 'DEBUG')

    def test_production_log_level(self):
        """The log level during production should be info."""
        # Create Session object.
        session = scheduled.Session(source='tmp/file.csv',
                                    profile='tmp_profile',
                                    scheduled='schd.xlsx',
                                    username='name',
                                    develop=False)

        self.assertEqual(_get_lvl(session._logger), 'INFO')
