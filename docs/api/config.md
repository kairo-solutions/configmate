# Config Class

The main configuration manager class.

## API Reference

For the full API, see the [source code](../../../configmate/config.py).

## Key Methods

- `set_default(key, value, type_hint=str)`: Set a default value for a configuration key.
- `require(key)`: Mark a configuration key as required.
- `validate(key, validator)`: Add a validation function for a configuration key.
- `load_from_env(prefix='', lowercase_keys=True, separator='__')`: Load configuration from environment variables.
- `load_from_file(file_path)`: Load configuration from a JSON or YAML file.
- `get(key, default=None)`: Get a configuration value, supporting nested keys.
- `set(key, value)`: Set a configuration value, supporting nested keys.
- `validate_all()`: Validate all configuration and return list of errors.
- `to_dict()`: Return the entire configuration as a dictionary.

## Nested Keys

ConfigMate supports nested keys using dot notation (e.g., `database.host`).

## Example

```python
from configmate import Config

config = Config()
config.set_default('debug', False, bool)
config.set_default('database.host', 'localhost', str)
config.load_from_env()  # Loads from environment variables

debug = config.get('debug')
host = config.get('database.host')
```