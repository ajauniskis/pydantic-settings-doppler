import os
from unittest.mock import MagicMock, patch

import pytest
from conftest import MockDopplerSDK
from dopplersdk.models.SecretsGetResponse import SecretsGetResponse
from pydantic_settings import BaseSettings
from pydantic_settings.sources import SettingsError

from pydantic_settings_doppler import DopplerSettingsSource


class TestDopplerSettingsSource:
    @patch("pydantic_settings_doppler.source.DopplerSDK", new=MockDopplerSDK)
    def test_initialization(self):
        source = DopplerSettingsSource(
            settings_cls=BaseSettings,
            token="mock-token",
            project_id="mock-project",
            config_id="mock-config",
        )
        assert source._project_id == "mock-project"
        assert source._config_id == "mock-config"

    @patch("pydantic_settings_doppler.source.DopplerSDK", new=MockDopplerSDK)
    def test_field_value_retrieval(self):
        class Settings(BaseSettings):
            database_url: str

        source = DopplerSettingsSource(
            settings_cls=Settings,
            token="mock-token",
            project_id="mock-project",
            config_id="mock-config",
        )
        source._client.secrets.get = MagicMock(
            return_value=SecretsGetResponse(
                value={"raw": "mocked-database_url"}  # pyright: ignore [reportArgumentType]
            )
        )
        values = source()
        assert values["database_url"] == "mocked-database_url"

    @patch("pydantic_settings_doppler.source.DopplerSDK", new=MockDopplerSDK)
    def test_missing_required_argument(self):
        class Settings(BaseSettings):
            api_key: str

        source = DopplerSettingsSource(
            settings_cls=Settings,
            token="mock-token",
            project_id="mock-project",
            config_id="mock-config",
        )
        source._client.secrets.get = MagicMock(return_value=None)
        with pytest.raises(SettingsError, match="api_key not found in Doppler"):
            source()

    @patch("pydantic_settings_doppler.source.DopplerSDK", new=MockDopplerSDK)
    def test_default_value_for_optional_field(self):
        class Settings(BaseSettings):
            optional_field: str = "default_value"

        source = DopplerSettingsSource(
            settings_cls=Settings,
            token="mock-token",
            project_id="mock-project",
            config_id="mock-config",
        )
        source._client.secrets.get = MagicMock(return_value=None)
        values = source()
        assert values["optional_field"] == "default_value"

    @patch("pydantic_settings_doppler.source.DopplerSDK", new=MockDopplerSDK)
    def test_missing_value_for_required_field(self):
        class Settings(BaseSettings):
            required_field: str

        source = DopplerSettingsSource(
            settings_cls=Settings,
            token="mock-token",
            project_id="mock-project",
            config_id="mock-config",
        )
        source._client.secrets.get = MagicMock(
            return_value=SecretsGetResponse(value={"raw": None})
        )
        with pytest.raises(SettingsError, match="required_field not found in Doppler"):
            source()

    @patch.dict(os.environ, {"DOPPLER_CONFIG_ID": "env-config-id"})
    @patch("pydantic_settings_doppler.source.DopplerSDK", new=MockDopplerSDK)
    def test_environment_variable_fallback(self):
        source = DopplerSettingsSource(
            settings_cls=BaseSettings,
            token="mock-token",
            project_id="mock-project",
        )
        assert source._config_id == "env-config-id"
