
class TestUtils:

    DUMMY_CONFIG = {
        "monitored_directory": "tests/resources/"
    }

class DummyConfig:
    def __getitem__(self, key):
        return TestUtils.DUMMY_CONFIG[key]

