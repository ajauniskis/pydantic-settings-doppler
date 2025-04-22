# Examples 🚀

This document provides practical examples of how to use `pydantic-settings-doppler` in various scenarios.

## Basic Example ✅

Retrieve secrets from Doppler and integrate them into a Pydantic settings model:

```python
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource
from pydantic_settings_doppler import DopplerSettingsSource

class AppSettings(BaseSettings):
    database_url: str
    api_key: str

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            DopplerSettingsSource(
                settings_cls,
                token="your-doppler-token",
                project_id="your-project-id",
                config_id="your-config-id",
            ),
        )

# Instantiate the settings
settings = AppSettings()
print(settings.database_url)
print(settings.api_key)
```

## Using Environment Variables 🌍

Set the required environment variables and retrieve them using `DopplerSettingsSource`:

```bash
export DOPPLER_TOKEN="your-doppler-access-token"
export DOPPLER_PROJECT_ID="your-project-id"
export DOPPLER_CONFIG_ID="your-config-id"
```

```python
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource
from pydantic_settings_doppler import DopplerSettingsSource

class AppSettings(BaseSettings):
    database_url: str
    api_key: str

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            DopplerSettingsSource(settings_cls),
        )

settings = AppSettings()
print(settings.database_url)
print(settings.api_key)
```

## Direct Initialization ⚙️

Pass Doppler configuration values directly to `DopplerSettingsSource`:

```python
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource
from pydantic_settings_doppler import DopplerSettingsSource

class AppSettings(BaseSettings):
    database_url: str
    api_key: str

    class Config:
        settings_customise_sources = lambda cls: [
            DopplerSettingsSource(
                cls,
                token="your-doppler-token",
                project_id="your-project-id",
                config_id="your-config-id",
            ),
            cls.env_settings_source,
        ]

settings = AppSettings()
print(settings.database_url)
print(settings.api_key)
```

## Error Handling Example 🚨

Handle missing required fields gracefully:

```python
from pydantic import ValidationError
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource
from pydantic_settings_doppler import DopplerSettingsSource

class AppSettings(BaseSettings):
    database_url: str
    api_key: str

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            DopplerSettingsSource(settings_cls),
        )

try:
    settings = AppSettings()
    print(settings.database_url)
    print(settings.api_key)
except ValidationError as e:
    print(f"Validation error: {e}")
```

## Logging Example 📝

Enable debug logging to troubleshoot Doppler integration:

```python
import logging

from pydantic_settings import BaseSettings, PydanticBaseSettingsSource
from pydantic_settings_doppler import DopplerSettingsSource
from pydantic_settings_doppler.logger import logger

logging.basicConfig(level=logging.DEBUG)
logger.setLevel(logging.DEBUG)


class AppSettings(BaseSettings):
    database_url: str
    api_key: str

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            DopplerSettingsSource(settings_cls),
        )


settings = AppSettings()
print(settings.database_url)
print(settings.api_key)

```

## Summary ✨

These examples demonstrate how to configure and use `pydantic-settings-doppler` in various scenarios, including basic usage, environment variable integration, direct initialization, customization, error handling, and logging.
