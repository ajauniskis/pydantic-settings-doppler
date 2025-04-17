import logging

from pydantic_settings_doppler.logger import logger


def test_logger_configuration():
    assert logger.name == "pydantic-settings-doppler"
    assert isinstance(logger, logging.Logger)
