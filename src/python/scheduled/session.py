import getpass
import logging
from logging.config import fileConfig
import os

from pandas import ExcelWriter

from scheduled.extractor import Extractor
from scheduled.utils import format_output, read_profile

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PROFILES_ROOT = os.path.join(PROJECT_ROOT, "profiles")
LOGGING_CONFIG = os.path.join(PROJECT_ROOT, "logging_config.ini")
fileConfig(LOGGING_CONFIG)


class Session:
    def __init__(
        self, source, profile, scheduled, dest, username=None, develop=False
    ):
        self.source = source
        self._given_profile = profile
        # A single _given_profile can have variations
        self.profiles = [
            os.path.join(PROFILES_ROOT, p)
            for p in os.listdir(PROFILES_ROOT)
            if p.startswith(profile)
        ]
        self.scheduled = scheduled
        self.dest = dest

        if username:
            self.username = username
        else:
            self.username = getpass.getuser()

        # setup logging
        if develop:
            self._logger = logging.getLogger("develop")
        else:
            self._logger = logging.getLogger("production")

        msg = "Session created on {self.source} ({self._given_profile}) by {self.username}".format(
            self=self
        )
        self._logger.info(msg)

    def run(self):
        extractor = Extractor.factory(os.path.splitext(self.source)[1])
        success = False

        for profile in self.profiles:
            with open(profile) as f:
                y = read_profile(f)
                mapping = y.get("mapping")
                options = y.get("options")

            df = extractor.extract(self.source, options)

            if not df.empty:
                self._logger.info(
                    "The following profile was used for extraction: "
                    + os.path.basename(profile)
                )
                success = True
                output_df = format_output(df, mapping)
                writer = ExcelWriter(self.dest)
                output_df.to_excel(writer, "Sheet1", index=False, header=False)
                writer.save()
                break

            if not success:
                self._logger.info(
                    "Unable to successfully extract data from the source"
                )
