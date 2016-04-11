
import json
import logging
import os

from arteria.exceptions import ArteriaUsageException
from arteria.web.state import State
from arteria.web.handlers import BaseRestHandler

from checksum import __version__ as version


log = logging.getLogger(__name__)

class BaseChecksumHandler(BaseRestHandler):
    """
    Base handler for checksum.
    """

    def initialize(self, config):
        """
        Ensures that any parameters feed to this are available
        to subclasses.
        """
        self.config = config


class VersionHandler(BaseChecksumHandler):
    """
    Get the version of the service
    """

    def get(self):
        """
        Returns the version of the checksum-service
        """
        self.write_object({"version": version })