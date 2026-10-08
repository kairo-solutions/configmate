# ConfigMate

![CI](https://img.shields.io/github/actions/workflow/status/kairo-solutions/configmate/ci.yml?branch=master)
![Version](https://img.shields.io/badge/version-0.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.7%20|%203.8%20|%203.9%20|%203.10%20|%203.11-blue)

A simple, powerful configuration management library for Python applications.

[**Read the documentation**](https://kairo-solutions.github.io/configmate/)

## Features

- Load configuration from multiple sources (environment variables, files, defaults)
- Automatic type conversion and validation
- Nested configuration support
- Easy to use API
- Zero required dependencies (optional PyYAML support for YAML files)
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

To load YAML configuration files, install the optional dependency:

```bash
pip install "configmate[yaml]"
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

## License

MIT

## Contributing

Bug reports and feature requests can be filed in the
[issue tracker](https://github.com/kairo-solutions/configmate/issues/new/choose).
See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidance on
preparing focused issues for Drips Wave.