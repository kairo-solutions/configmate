# ConfigMate

A simple, powerful configuration management library for Python applications.

## Features

- Load configuration from multiple sources (environment variables, files, defaults)
- Automatic type conversion and validation
- Nested configuration support
- Easy to use API
- Zero required dependencies; install `configmate[yaml]` for YAML file support
- **Stellar-specific configuration loading** (optional)

## About Kairo Solutions

ConfigMate is maintained by Kairo Solutions, a technology organization focused on building reliable, developer-friendly open source tools. Our mission is to simplify complex development challenges through well-designed, intuitive libraries that integrate seamlessly into modern Python workflows.

We believe in:

- **Simplicity without sacrifice**: Powerful features that don't complicate the developer experience
- **Reliability**: Thoroughly tested, stable releases you can depend on in production
- **Community-driven development**: Transparent processes that welcome contributions from developers worldwide
- **Practical solutions**: Tools designed to solve real-world problems faced by Python developers daily

## Installation

```bash
pip install configmate
```

## Usage

### Basic Usage

```python
from configmate import Config

config = Config()
config.load_from_env(prefix='APP_')
config.load_from_file('config.yaml')
config.set_default('debug', False, bool)

debug = config.get('debug')
database_url = config.get('database.url')
```

### Stellar Configuration

ConfigMate includes optional Stellar-specific configuration loading for applications that interact with the Stellar network.

```python
from configmate import StellarConfig

# Create a Stellar configuration instance
stellar_config = StellarConfig()

# Load from environment variables with STELLAR_ prefix
# e.g., STELLAR_NETWORK=mainnet STELLAR_HORIZON_URL=https://custom.horizon.example
stellar_config.load_from_env()

# Get the horizon URL for the current network
horizon_url = stellar_config.get_horizon_url()

# Check if using a known network
if stellar_config.is_known_network():
    print(f"Using known network: {stellar_config.get('stellar.network')}")
else:
    print(f"Using custom network: {stellar_config.get('stellar.network')}")

# Access other configuration values as usual
network = stellar_config.get('stellar.network')
```

The `StellarConfig` class extends `Config` and provides:

- Defaults for `stellar.network` (testnet) and `stellar.horizon_url` (based on network)
- Automatic loading from environment variables with `STELLAR_` prefix
- Validation for the network field
- Helper methods like `get_horizon_url()` and `is_known_network()`

## Documentation

For more detailed documentation, please refer to the following sections:

- [Configuration](configuration/usage.md)
- [Stellar Configuration](configuration/stellar.md)
- [API Reference](api/config.md)
- [Examples](examples/basic.md)

## License

MIT