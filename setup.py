from setuptools import setup, find_packages
from checksum import __version__
import os


def read_file(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


try:
    with open("requirements/prod", "r") as f:
        install_requires = [x.strip() for x in f.readlines()]
except IOError:
    install_requires = []

setup(
    name='checksum',
    version=__version__,
    description="Micro-service for checking checksums",
    long_description=read_file('README.md'),
    keywords='bioinformatics',
    author='SNP&SEQ Technology Platform, Uppsala University',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': ['checksum-ws = checksum.app:start']
    },
)
