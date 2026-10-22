# Configuration Usage

## Basic Usage

```python
from configmate import Config

config = Config()
config.load_from_env(prefix='APP_')
config.load_from_file('config.yaml')
config.set_default('debug', False, bool)

debug = config.get('debug')
database_url = config.get('database.url')
```

## Features

- Load configuration from multiple sources (environment variables, files, defaults)
- Automatic type conversion and validation
- Nested configuration support
- Easy to use API
- Zero required dependencies; install `kairo-configmate[yaml]` for YAML file support

## Supported File Formats

`load_from_file()` supports JSON (`.json`) and YAML (`.yaml`, `.yml`).
Extensions are case-insensitive. YAML requires the optional
`kairo-configmate[yaml]` dependency.

JSONC (`.jsonc`) is not supported, even when the file contains no comments.
Loading an existing `.jsonc` file raises
`ValueError: Unsupported file format: .jsonc` rather than attempting JSON parsing.
To use a JSONC configuration, remove its comments and any other non-JSON syntax,
then save the resulting valid JSON with a `.json` extension.

## API Reference

For the full API reference, see the [API Reference](../api/config.md) section.