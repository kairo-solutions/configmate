# Basic Usage Example

This example shows how to use ConfigMate for general configuration management.

```python
from configmate import Config

# Create a configuration instance
config = Config()

# Load configuration from environment variables with prefix 'APP_'
config.load_from_env(prefix='APP_')

# Load configuration from a file (JSON or YAML)
config.load_from_file('config.yaml')

# Set default values
config.set_default('debug', False, bool)
config.set_default('database.host', 'localhost', str)
config.set_default('database.port', 5432, int)

# Access configuration values
debug = config.get('debug')
database_host = config.get('database.host')
database_port = config.get('database.port')

# Set configuration values programmatically
config.set('debug', True)
config.set('database.host', 'production-server')
```

## Nested Configuration

ConfigMate supports nested keys using dot notation.

```python
config.set('database.credentials.username', 'admin')
config.set('database.credentials.password', 'secret')

username = config.get('database.credentials.username')
# Returns: 'admin'
```