
import json

from tornado.testing import *
from tornado.web import Application

from checksum.app import routes
from checksum import __version__ as checksum_version
from tests.test_utils import DummyConfig

class TestChecksumHandlers(AsyncHTTPTestCase):

    API_BASE="/api/1.0"

    def get_app(self):
        return Application(routes(config=DummyConfig()))

    def test_start_checksum(self):
        pass

    def test_check_status(self):
        pass

    def test_stop_checksum(self):
        pass

    def test_version(self):
        response = self.fetch(self.API_BASE + "/version")

        expected_result = { "version": checksum_version }

        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body), expected_result)

