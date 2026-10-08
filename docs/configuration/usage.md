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
- Zero dependencies

## API Reference

For the full API reference, see the [API Reference](../api/config.md) section.