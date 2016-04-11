
import json
import mock

from tornado.testing import *
from tornado.web import Application
from tornado.escape import json_encode

from arteria.web.state import State

from checksum.app import routes
from checksum import __version__ as checksum_version
from checksum.lib.jobrunner import LocalQAdapter
from tests.test_utils import DummyConfig

"""

"""
class TestChecksumHandlers(AsyncHTTPTestCase):

    API_BASE="/api/1.0"

    runner_service = LocalQAdapter(nbr_of_cores=2, interval = 2, priority_method = "fifo")

    def get_app(self):
        return Application(
            routes(
                config=DummyConfig(),
                runner_service=self.runner_service))

    def test_start_checksum(self):
        body = {"path_to_md5_sum_file": "tests/resources/ok_checksums/md5_checksums"}
        response = self.fetch(
            self.API_BASE + "/start/ok_checksums",
            method="POST",
            body=json_encode(body))

        response_as_json = json.loads(response.body)

        # TODO if we want more tests on the same
        #      server, this needs to become
        #      a global variable.
        job_id = 1

        self.assertEqual(response.code, 202)
        self.assertEqual(response_as_json["job_id"], job_id)
        self.assertEqual(response_as_json["service_version"], checksum_version)

        expected_link = "http://localhost:{0}/api/1.0/status/{1}".format(self.get_http_port(), job_id)
        self.assertEqual(response_as_json["link"], expected_link)
        self.assertEqual(response_as_json["state"], State.STARTED)


    def test_start_checksum_with_shell_injection(self):
        body = {"path_to_md5_sum_file": "tests/$(cat /etc/shadow)"}
        response = self.fetch(
            self.API_BASE + "/start/ok_checksums",
            method="POST",
            body=json_encode(body))

        self.assertEqual(response.code, 500)


    def test_check_status(self):
        with mock.patch("checksum.lib.jobrunner.LocalQAdapter.status", return_value=State.DONE) as m:
            response = self.fetch(self.API_BASE + "/status/1")
            response_as_json = json.loads(response.body)
            self.assertEqual(response_as_json["state"], State.DONE)
            m.assert_called_with("1")

    def test_stop_all_checksum(self):
        with mock.patch("checksum.lib.jobrunner.LocalQAdapter.stop_all") as m:
            response = self.fetch(self.API_BASE + "/stop/all", method="POST", body="")
            self.assertEqual(response.code, 200)
            m.assert_called_with()


    def test_stop_one_checksum(self):
        with mock.patch("checksum.lib.jobrunner.LocalQAdapter.stop") as m:
            response = self.fetch(self.API_BASE + "/stop/1", method="POST", body="")
            self.assertEqual(response.code, 200)
            m.assert_called_with("1")

    def test_version(self):
        response = self.fetch(self.API_BASE + "/version")

        expected_result = { "version": checksum_version }

        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body), expected_result)

