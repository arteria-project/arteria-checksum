
import json
import logging
import os

from arteria.exceptions import ArteriaUsageException
from arteria.web.state import State
from arteria.web.handlers import BaseRestHandler

from checksum import __version__ as version
from checksum.lib.jobrunner import LocalQAdapter

log = logging.getLogger(__name__)

class BaseChecksumHandler(BaseRestHandler):
    """
    Base handler for checksum.
    """

    def initialize(self, config, runner_service):
        """
        Ensures that any parameters feed to this are available
        to subclasses.
        """
        self.config = config
        # TODO Load runnner service from config!
        self.runner_service = runner_service


class VersionHandler(BaseChecksumHandler):

    """
    Get the version of the service
    """
    def get(self):
        """
        Returns the version of the checksum-service
        """
        self.write_object({"version": version })


class StartHandler(BaseChecksumHandler):

    """
    Validate that the runfolder exists under monitored directories
    :param runfolder: The runfolder to check for
    :param monitored_dir: The root in which the runfolder should exist
    :return: True if this is a valid runfolder
    """
    @staticmethod
    def _validate_runfolder_exists(runfolder, monitored_dir):
        if os.path.isdir(monitored_dir):
            sub_folders = [ name for name in os.listdir(monitored_dir)
                            if os.path.isdir(os.path.join(monitored_dir, name)) ]
            return runfolder in sub_folders
        else:
            return False

    """
    Start a checksumming process.

    The request needs to pass the path the md5 sum file to check in "path_to_md5_sum_file". This path
    has to point to a file in the runfolder.

    :param runfolder: name of the runfolder we want to start bcl2fastq for

    """
    def post(self, runfolder):

        monitored_dir = self.config["monitored_directory"]
        StartHandler._validate_runfolder_exists(runfolder, monitored_dir)

        request_data = json.loads(self.request.body)

        path_to_md5_sum_file = os.path.abspath(request_data["path_to_md5_sum_file"])

        if not os.path.isfile(path_to_md5_sum_file):
            raise ArteriaUsageException("{} is not a file!".format(path_to_md5_sum_file))

        #md5sum_file = self.request.body["md5sum_file"]
        #start(self, cmd, nbr_of_cores, run_dir, stdout=None, stderr=None)
        cmd = " ".join(["md5sum -c", path_to_md5_sum_file])
        print cmd
        print os.path.abspath(monitored_dir)
        print path_to_md5_sum_file
        job_id = self.runner_service.start(cmd, nbr_of_cores=1, run_dir=monitored_dir, stdout=None, stderr=None)

        status_end_point = "{0}://{1}{2}".format(
            self.request.protocol,
            self.request.host,
            self.reverse_url("status", job_id))

        response_data = {
                "job_id": job_id,
                "service_version": version,
                "link": status_end_point,
                "state": State.STARTED}

        self.set_status(202, reason="started processing")
        self.write_object(response_data)


class StatusHandler(BaseChecksumHandler):
    """
    Get the status of one or all jobs.
    """

    def get(self, job_id):
        """
        Get the status of the specified job_id, or if now id is given, the
        status of all jobs.
        :param job_id: to check status for (set to empty to get status for all)
        """

        if job_id:
            status = {"state": self.runner_service.status(job_id)}
        else:
            all_status = self.runner_service.status_all()
            status_dict = {}
            for k,v in all_status.iteritems():
                status_dict[k] = {"state": v}
            status = status_dict

        self.write_json(status)

