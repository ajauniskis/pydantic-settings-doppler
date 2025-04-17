from unittest.mock import MagicMock


class MockDopplerSDK:
    def __init__(self, **kwargs):
        self.secrets = MagicMock()
