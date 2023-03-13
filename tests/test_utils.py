import os
import pytest
import subprocess
import tempfile


DUMMY_CONFIG = {
    "monitored_directory": "/tmp",
    "md5_log_directory": "/tmp",
    "history_len": 10,
    "port": 9999,
}


class DummyConfig:
    def __getitem__(self, key):
        return DUMMY_CONFIG[key]


def gen_dummy_data(filesize=10**4, n_files=5):
    """
    Initialize a folder containing a set of files and their checksum

    Parameters
    ----------
    filesize: int
        size of each file
    n_files: int
        number of files to create

    Return
    ------
    (Folder, checksum_file): (Folder, str)
        Temporary Folder containing the files, as well as the name of the file
        containing the checksums.
    """
    folder = tempfile.TemporaryDirectory(
            dir=DUMMY_CONFIG["monitored_directory"])

    for i in range(n_files):
        filename = "/".join([folder.name, f"file{i}.bin"])
        with open(filename, 'wb') as f:
            f.write(os.urandom(filesize))

        with open("/".join([folder.name, "md5_checksums"]), 'a') as f:
            subprocess.run(
                    ["md5sum", "/".join(filename.split("/")[-2:])],
                    cwd=DUMMY_CONFIG["monitored_directory"],
                    stdout=f)

    return folder, "md5_checksums"
