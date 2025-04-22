# Configuration ⚙️

## Overview 🌟

This document explains how to configure `pydantic-settings-doppler` to retrieve secrets from Doppler.

## Environment Variables 🌍

To use `DopplerSettingsSource`, you need to configure the following environment variables:

- **`DOPPLER_TOKEN`**: Your Doppler access token. This is required to authenticate with the Doppler API.
- **`DOPPLER_PROJECT_ID`**: The ID of your Doppler project. This identifies the project from which secrets will be retrieved.
- **`DOPPLER_CONFIG_ID`**: The ID of your Doppler configuration. This specifies the configuration environment (e.g., development, staging, production).

### Example ✅

Set the environment variables in your shell:

```bash
export DOPPLER_TOKEN="your-doppler-access-token"
export DOPPLER_PROJECT_ID="your-project-id"
export DOPPLER_CONFIG_ID="your-config-id"
```

Alternatively, you can use a `.env` file:

```env
DOPPLER_TOKEN=your-doppler-access-token
DOPPLER_PROJECT_ID=your-project-id
DOPPLER_CONFIG_ID=your-config-id
```

## Direct Initialization 🛠️

You can also pass the configuration values directly to `DopplerSettingsSource` when initializing it:

```python
from pydantic_settings_doppler import DopplerSettingsSource

source = DopplerSettingsSource(
    settings_cls=AppSettings,
    token="your-doppler-token",
    project_id="your-project-id",
    config_id="your-config-id",
)
```

## Error Handling 🚨

If a required field is not found in Doppler, a `ValidationError` will be raised. Ensure all required secrets are present in your Doppler configuration.

If any of config variables are not found either in environment variables on not passed in the constructor, a `SettingsError` will be raised.

## Logging Configuration 📝

`pydantic-settings-doppler` uses Python's `logging` module to provide debug and warning messages. To enable debug logging, configure the logger:

```python
import logging
from pydantic_settings_doppler.logger import logger

logging.basicConfig(level=logging.DEBUG)
logger.setLevel(logging.DEBUG)
```

## Advanced Configuration 🔧

### Customizing Field Names

By default, `DopplerSettingsSource` uses the field name in uppercase as the key to retrieve secrets from Doppler. You can customize this behavior by setting the `alias` or `serialization_alias` attribute in your Settings model:

```python
from pydantic import Field
from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    db_url: str = Field(alias="DATABASE_URL")
    api_key: str
```
